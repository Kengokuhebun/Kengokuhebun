"use client";
import { AlertTriangle, Film, ImageIcon, PenLine, Trash2, UploadCloud, X } from "lucide-react";
import { useCallback, useRef, useState } from "react";
import type { AppConfig } from "@/lib/client/api";
import {
  ACCEPT,
  classifyFile,
  classifyRatio,
  displayName,
  formatBytes,
  MAX_IMAGE,
  MAX_VIDEO,
  mediaUrl,
  probeDimensions,
  uploadFile,
} from "@/lib/client/upload";
import type { Asset } from "@/lib/launch/schema";
import { useStore } from "@/lib/store";
import { Badge, Button, cn, Input, Section, Segmented, Textarea } from "../ui";

interface QueueItem {
  id: string;
  fileName: string;
  progress: number;
  error?: string;
}

const CONCURRENCY = 3;

export function MediaSection({ appConfig }: { appConfig: AppConfig | null }) {
  const assets = useStore((s) => s.assets);
  const addAsset = useStore((s) => s.addAsset);
  const clearAssets = useStore((s) => s.clearAssets);
  const setAllIncluded = useStore((s) => s.setAllIncluded);
  const [queue, setQueue] = useState<QueueItem[]>([]);
  const [dragging, setDragging] = useState(false);
  const [filter, setFilter] = useState<"all" | "1:1" | "4:5" | "9:16" | "other">("all");
  const inputRef = useRef<HTMLInputElement>(null);

  const patchQueue = (id: string, patch: Partial<QueueItem>) =>
    setQueue((q) => q.map((x) => (x.id === id ? { ...x, ...patch } : x)));

  const handleFiles = useCallback(
    async (files: File[]) => {
      if (!appConfig) return;
      const jobs: { item: QueueItem; file: File }[] = [];
      const fresh: QueueItem[] = [];
      for (const file of files) {
        const item: QueueItem = { id: crypto.randomUUID(), fileName: file.name, progress: 0 };
        const type = classifyFile(file);
        if (!type) item.error = "Not allowed. Use .mp4, .mov, .jpg or .png";
        else if (type.kind === "image" && file.size > MAX_IMAGE) item.error = "Image is over Meta's 30 MB limit";
        else if (type.kind === "video" && file.size > MAX_VIDEO) item.error = "Video is over Meta's 4 GB limit";
        else jobs.push({ item, file });
        fresh.push(item);
      }
      setQueue((q) => [...q, ...fresh]);

      let next = 0;
      const worker = async () => {
        while (next < jobs.length) {
          const { item, file } = jobs[next++];
          const type = classifyFile(file)!;
          try {
            const dims = await probeDimensions(file, type.kind);
            const { storageKey } = await uploadFile(file, type.mime, appConfig, (p) => patchQueue(item.id, { progress: p }));
            const asset: Asset = {
              id: item.id,
              storageKey,
              name: displayName(file.name),
              fileName: file.name,
              kind: type.kind,
              mime: type.mime,
              width: dims.width,
              height: dims.height,
              size: file.size,
              ratio: classifyRatio(dims.width, dims.height),
              included: true,
              overrides: {},
            };
            addAsset(asset);
            setQueue((q) => q.filter((x) => x.id !== item.id));
          } catch (e) {
            patchQueue(item.id, { error: (e as Error).message });
          }
        }
      };
      await Promise.all(Array.from({ length: Math.min(CONCURRENCY, jobs.length) }, worker));
    },
    [appConfig, addAsset],
  );

  const included = assets.filter((a) => a.included).length;
  const shown = assets.filter((a) => filter === "all" || a.ratio === filter);
  const counts = (r: string) => assets.filter((a) => a.ratio === r).length;

  return (
    <Section
      step={1}
      id="media"
      title="Creatives"
      description="Drop .mp4, .mov, .jpg or .png files. Best ratios: 1:1, 4:5, 9:16."
      right={
        assets.length ? (
          <div className="flex items-center gap-1.5">
            <Badge tone="dark">
              {included} of {assets.length} selected
            </Badge>
          </div>
        ) : null
      }
    >
      <div
        onDragOver={(e) => {
          e.preventDefault();
          setDragging(true);
        }}
        onDragLeave={() => setDragging(false)}
        onDrop={(e) => {
          e.preventDefault();
          setDragging(false);
          void handleFiles(Array.from(e.dataTransfer.files));
        }}
        onClick={() => inputRef.current?.click()}
        role="button"
        tabIndex={0}
        onKeyDown={(e) => (e.key === "Enter" || e.key === " ") && inputRef.current?.click()}
        className={cn(
          "flex cursor-pointer flex-col items-center justify-center rounded-xl border-2 border-dashed px-6 py-8 text-center transition-colors",
          dragging ? "border-primary bg-primary/5" : "hover:border-foreground/30 hover:bg-muted/50",
        )}
      >
        <UploadCloud className="mb-2 h-8 w-8 text-muted-foreground" />
        <div className="text-sm font-medium">Drag and drop creatives here, or click to choose</div>
        <div className="mt-1 text-xs text-muted-foreground">
          Bulk upload is fine. Files go to {appConfig?.storage === "supabase" ? "Supabase Storage" : "this computer (local storage)"}.
        </div>
        <input
          ref={inputRef}
          type="file"
          multiple
          accept={ACCEPT}
          className="hidden"
          data-testid="file-input"
          onChange={(e) => {
            void handleFiles(Array.from(e.target.files ?? []));
            e.target.value = "";
          }}
        />
      </div>

      {queue.length ? (
        <div className="mt-4 space-y-1.5">
          {queue.map((q) => (
            <div key={q.id} className="flex items-center gap-3 rounded-md border px-3 py-2 text-sm">
              <span className="min-w-0 flex-1 truncate">{q.fileName}</span>
              {q.error ? (
                <>
                  <span className="text-xs text-danger">{q.error}</span>
                  <button className="text-muted-foreground hover:text-foreground" onClick={() => setQueue((x) => x.filter((i) => i.id !== q.id))} aria-label="Dismiss">
                    <X className="h-4 w-4" />
                  </button>
                </>
              ) : (
                <div className="h-1.5 w-40 overflow-hidden rounded-full bg-muted">
                  <div className="h-full bg-primary transition-all" style={{ width: `${Math.max(4, q.progress * 100)}%` }} />
                </div>
              )}
            </div>
          ))}
        </div>
      ) : null}

      {assets.length ? (
        <>
          <div className="mt-5 flex flex-wrap items-center justify-between gap-2">
            <Segmented
              value={filter}
              onChange={setFilter}
              options={[
                { value: "all", label: `All ${assets.length}` },
                { value: "1:1", label: `1:1 · ${counts("1:1")}` },
                { value: "4:5", label: `4:5 · ${counts("4:5")}` },
                { value: "9:16", label: `9:16 · ${counts("9:16")}` },
                ...(counts("other") ? [{ value: "other" as const, label: `Other · ${counts("other")}` }] : []),
              ]}
            />
            <div className="flex gap-1.5">
              <Button variant="ghost" size="sm" onClick={() => setAllIncluded(true)}>
                Select all
              </Button>
              <Button variant="ghost" size="sm" onClick={() => setAllIncluded(false)}>
                Select none
              </Button>
              <Button
                variant="ghost"
                size="sm"
                className="text-danger"
                onClick={() => {
                  if (confirm("Remove all creatives from this launch? Files stay in storage.")) clearAssets();
                }}
              >
                Clear all
              </Button>
            </div>
          </div>
          <div className="mt-3 grid grid-cols-2 gap-3 sm:grid-cols-3 lg:grid-cols-4 2xl:grid-cols-5">
            {shown.map((a) => (
              <AssetCard key={a.id} asset={a} />
            ))}
          </div>
        </>
      ) : null}
    </Section>
  );
}

function AssetCard({ asset }: { asset: Asset }) {
  const updateAsset = useStore((s) => s.updateAsset);
  const removeAsset = useStore((s) => s.removeAsset);
  const [editing, setEditing] = useState(false);
  const [broken, setBroken] = useState(false);
  const hasOverrides = Object.values(asset.overrides ?? {}).some((v) => v?.trim());
  const aspect = asset.width && asset.height ? `${asset.width} / ${asset.height}` : "1 / 1";

  return (
    <div className={cn("group flex flex-col overflow-hidden rounded-lg border bg-card transition-opacity", !asset.included && "opacity-55")}>
      <div className="relative flex aspect-[4/5] items-center justify-center overflow-hidden bg-[#111]">
        {broken ? (
          <div className="px-3 text-center text-xs text-white/70">Preview not available. The file may have been removed.</div>
        ) : asset.kind === "image" ? (
          // eslint-disable-next-line @next/next/no-img-element
          <img src={mediaUrl(asset.storageKey)} alt={asset.name} className="max-h-full max-w-full object-contain" style={{ aspectRatio: aspect }} onError={() => setBroken(true)} />
        ) : (
          <video
            src={mediaUrl(asset.storageKey)}
            className="max-h-full max-w-full object-contain"
            muted
            loop
            playsInline
            preload="metadata"
            onMouseEnter={(e) => void e.currentTarget.play().catch(() => {})}
            onMouseLeave={(e) => e.currentTarget.pause()}
            onError={() => setBroken(true)}
          />
        )}
        <label className="absolute left-2 top-2 flex cursor-pointer items-center rounded-md bg-white/95 p-1 shadow">
          <input
            type="checkbox"
            className="h-4 w-4 cursor-pointer accent-[var(--primary)]"
            checked={asset.included}
            onChange={(e) => updateAsset(asset.id, { included: e.target.checked })}
            aria-label={`Include ${asset.name}`}
          />
        </label>
        <button
          className="absolute right-2 top-2 rounded-md bg-white/95 p-1 text-muted-foreground opacity-0 shadow transition-opacity hover:text-danger group-hover:opacity-100 focus:opacity-100"
          onClick={() => {
            removeAsset(asset.id);
            void fetch(`/api/media/file?key=${encodeURIComponent(asset.storageKey)}`, { method: "DELETE" });
          }}
          aria-label={`Remove ${asset.name}`}
          title="Remove and delete the file"
        >
          <Trash2 className="h-4 w-4" />
        </button>
        <div className="absolute bottom-2 left-2 flex gap-1">
          <Badge tone={asset.ratio === "other" ? "amber" : "dark"} className="bg-black/70 text-white">
            {asset.ratio === "other" ? (
              <>
                <AlertTriangle className="h-3 w-3" /> {asset.width ? `${asset.width}×${asset.height}` : "unknown size"}
              </>
            ) : (
              asset.ratio
            )}
          </Badge>
          <Badge className="bg-black/70 text-white">
            {asset.kind === "video" ? <Film className="h-3 w-3" /> : <ImageIcon className="h-3 w-3" />}
            {formatBytes(asset.size)}
          </Badge>
        </div>
      </div>
      <div className="space-y-2 p-2.5">
        <Input
          value={asset.name}
          onChange={(e) => updateAsset(asset.id, { name: e.target.value })}
          className="h-8 text-xs font-medium"
          aria-label="Creative name"
          title="Creative name, used in {creative}"
        />
        <button
          onClick={() => setEditing((v) => !v)}
          className={cn("flex w-full items-center gap-1.5 text-xs text-muted-foreground hover:text-foreground", hasOverrides && "text-primary")}
        >
          <PenLine className="h-3 w-3" />
          {hasOverrides ? "Custom copy for this ad" : "Use different copy for this ad"}
        </button>
        {editing ? (
          <div className="space-y-1.5">
            <Textarea
              className="min-h-16 text-xs"
              placeholder="Primary text (blank = use main copy)"
              value={asset.overrides?.primaryText ?? ""}
              onChange={(e) => updateAsset(asset.id, { overrides: { ...asset.overrides, primaryText: e.target.value } })}
            />
            <Input
              className="h-8 text-xs"
              placeholder="Headline (blank = main)"
              value={asset.overrides?.headline ?? ""}
              onChange={(e) => updateAsset(asset.id, { overrides: { ...asset.overrides, headline: e.target.value } })}
            />
            <Input
              className="h-8 text-xs"
              placeholder="Link (blank = main)"
              value={asset.overrides?.link ?? ""}
              onChange={(e) => updateAsset(asset.id, { overrides: { ...asset.overrides, link: e.target.value } })}
            />
          </div>
        ) : null}
      </div>
    </div>
  );
}
