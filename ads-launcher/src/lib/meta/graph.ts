import crypto from "node:crypto";

/**
 * Minimal Meta Graph API client. Server-side only (it holds the token).
 * - Form-encodes params; objects/arrays are JSON-encoded, as Graph expects.
 * - Retries transient and rate-limit errors with backoff.
 * - Never includes the access token in errors or logs.
 */

export interface GraphOptions {
  token: string;
  version: string;
  base: string;
  appSecret?: string;
  fetchImpl?: typeof fetch;
  sleep?: (ms: number) => Promise<void>;
  maxRetries?: number;
}

export class MetaApiError extends Error {
  status: number;
  code?: number;
  subcode?: number;
  type?: string;
  userTitle?: string;
  userMessage?: string;
  fbtraceId?: string;
  transient: boolean;

  constructor(status: number, body: unknown, fallback: string) {
    const e = (body as { error?: Record<string, unknown> })?.error ?? {};
    const userMsg = (e.error_user_msg as string) || "";
    const msg = (e.message as string) || fallback;
    super(userMsg ? `${msg} ${userMsg}`.trim() : msg);
    this.name = "MetaApiError";
    this.status = status;
    this.code = e.code as number | undefined;
    this.subcode = e.error_subcode as number | undefined;
    this.type = e.type as string | undefined;
    this.userTitle = e.error_user_title as string | undefined;
    this.userMessage = userMsg || undefined;
    this.fbtraceId = e.fbtrace_id as string | undefined;
    this.transient =
      Boolean(e.is_transient) ||
      status >= 500 ||
      [1, 2, 4, 17, 32, 341, 613].includes(this.code ?? -1) ||
      (this.code !== undefined && this.code >= 80000 && this.code <= 80014);
  }

  /** Everything useful for debugging, as one line. */
  describe(): string {
    const bits = [this.message];
    if (this.userTitle) bits.unshift(`${this.userTitle}:`);
    const codes = [this.code && `code ${this.code}`, this.subcode && `subcode ${this.subcode}`]
      .filter(Boolean)
      .join(", ");
    if (codes) bits.push(`(${codes})`);
    if (this.fbtraceId) bits.push(`trace ${this.fbtraceId}`);
    return bits.join(" ");
  }
}

function encodeValue(v: unknown): string {
  if (typeof v === "string") return v;
  if (typeof v === "number" || typeof v === "boolean") return String(v);
  return JSON.stringify(v);
}

export class GraphClient {
  private opts: Required<Omit<GraphOptions, "appSecret">> & { appSecret?: string };

  constructor(opts: GraphOptions) {
    this.opts = {
      fetchImpl: opts.fetchImpl ?? fetch,
      sleep: opts.sleep ?? ((ms) => new Promise((r) => setTimeout(r, ms))),
      maxRetries: opts.maxRetries ?? 3,
      ...opts,
    } as GraphClient["opts"];
  }

  private url(path: string): string {
    const p = path.startsWith("/") ? path : `/${path}`;
    return `${this.opts.base}/${this.opts.version}${p}`;
  }

  private authParams(): Record<string, string> {
    const params: Record<string, string> = { access_token: this.opts.token };
    if (this.opts.appSecret) {
      params.appsecret_proof = crypto
        .createHmac("sha256", this.opts.appSecret)
        .update(this.opts.token)
        .digest("hex");
    }
    return params;
  }

  private async request<T>(method: "GET" | "POST" | "DELETE", path: string, build: () => RequestInit & { query?: URLSearchParams }): Promise<T> {
    let attempt = 0;
    for (;;) {
      const init = build();
      const url = new URL(this.url(path));
      if (init.query) init.query.forEach((v, k) => url.searchParams.set(k, v));
      let res: Response;
      try {
        res = await this.opts.fetchImpl(url.toString(), { method, body: init.body, headers: init.headers });
      } catch (err) {
        if (attempt < this.opts.maxRetries) {
          attempt += 1;
          await this.opts.sleep(1000 * 2 ** attempt);
          continue;
        }
        throw new Error(`Network error talking to Meta: ${(err as Error).message}`);
      }
      const text = await res.text();
      let body: unknown = null;
      try {
        body = text ? JSON.parse(text) : null;
      } catch {
        body = { error: { message: text.slice(0, 300) } };
      }
      if (res.ok && !(body as { error?: unknown })?.error) return body as T;
      const err = new MetaApiError(res.status, body, `HTTP ${res.status}`);
      if (err.transient && attempt < this.opts.maxRetries) {
        attempt += 1;
        await this.opts.sleep(1000 * 2 ** attempt);
        continue;
      }
      throw err;
    }
  }

  get<T = Record<string, unknown>>(path: string, params: Record<string, unknown> = {}): Promise<T> {
    return this.request<T>("GET", path, () => {
      const query = new URLSearchParams(this.authParams());
      for (const [k, v] of Object.entries(params)) if (v !== undefined) query.set(k, encodeValue(v));
      return { query };
    });
  }

  post<T = Record<string, unknown>>(path: string, params: Record<string, unknown> = {}): Promise<T> {
    return this.request<T>("POST", path, () => {
      const body = new URLSearchParams(this.authParams());
      for (const [k, v] of Object.entries(params)) if (v !== undefined) body.set(k, encodeValue(v));
      return { body, headers: { "content-type": "application/x-www-form-urlencoded" } };
    });
  }

  /** Multipart upload, e.g. a video file as `source`. */
  postMultipart<T = Record<string, unknown>>(
    path: string,
    fields: Record<string, string>,
    file?: { field: string; data: Uint8Array; fileName: string; mime: string },
  ): Promise<T> {
    return this.request<T>("POST", path, () => {
      const form = new FormData();
      for (const [k, v] of Object.entries({ ...this.authParams(), ...fields })) form.set(k, v);
      if (file) {
        const blob = new Blob([file.data as BlobPart], { type: file.mime });
        form.set(file.field, blob, file.fileName);
      }
      return { body: form };
    });
  }

  /** Follows `paging.next` cursors up to `max` items. */
  async getAll<T>(path: string, params: Record<string, unknown> = {}, max = 500): Promise<T[]> {
    const out: T[] = [];
    let after: string | undefined;
    for (;;) {
      const page = await this.get<{ data?: T[]; paging?: { cursors?: { after?: string }; next?: string } }>(path, {
        limit: 100,
        ...params,
        ...(after ? { after } : {}),
      });
      out.push(...(page.data ?? []));
      after = page.paging?.cursors?.after;
      if (!page.paging?.next || !after || out.length >= max) break;
    }
    return out.slice(0, max);
  }
}
