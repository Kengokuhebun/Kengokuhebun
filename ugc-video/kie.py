"""kie.ai helper for the UGC videos.

The API key is never stored here. In the cloud session a network proxy adds it;
locally, set KIE_API_KEY in your environment.

  python3 kie.py create <model> '<input json>'   -> prints taskId
  python3 kie.py wait <taskId> [outdir]           -> waits, prints result URLs, downloads them
  python3 kie.py credits
"""
import json
import os
import sys
import time
import urllib.request

API = "https://api.kie.ai/api/v1"


def _req(url, body=None):
    key = os.environ.get("KIE_API_KEY", "proxy-injected")
    data = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request(url, data=data, method="POST" if data else "GET")
    req.add_header("Authorization", f"Bearer {key}")
    req.add_header("Content-Type", "application/json")
    with urllib.request.urlopen(req, timeout=120) as r:
        return json.loads(r.read())


def create(model, inp):
    res = _req(f"{API}/jobs/createTask", {"model": model, "input": inp})
    if res.get("code") != 200:
        raise SystemExit(f"createTask failed: {res}")
    return res["data"]["taskId"]


def wait(task_id, outdir=None, timeout=1800):
    start, delay = time.time(), 3
    while True:
        d = _req(f"{API}/jobs/recordInfo?taskId={task_id}")["data"]
        state = d.get("state")
        if state == "success":
            urls = json.loads(d["resultJson"]).get("resultUrls", [])
            paths = []
            if outdir:
                os.makedirs(outdir, exist_ok=True)
                for i, u in enumerate(urls):
                    ext = os.path.splitext(u.split("?")[0])[1] or ".bin"
                    p = os.path.join(outdir, f"{task_id}_{i}{ext}")
                    urllib.request.urlretrieve(u, p)
                    paths.append(p)
            return {"urls": urls, "paths": paths, "credits": d.get("creditsConsumed"), "secs": d.get("costTime")}
        if state == "fail":
            raise SystemExit(f"task {task_id} failed: {d.get('failCode')} {d.get('failMsg')}")
        if time.time() - start > timeout:
            raise SystemExit(f"task {task_id} timed out in state {state}")
        time.sleep(delay)
        delay = min(delay * 1.5, 20)


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "credits":
        print(_req(f"{API}/chat/credit")["data"])
    elif cmd == "create":
        print(create(sys.argv[2], json.loads(sys.argv[3])))
    elif cmd == "wait":
        print(json.dumps(wait(sys.argv[2], sys.argv[3] if len(sys.argv) > 3 else None), indent=1))
