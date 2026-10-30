"""Small kie.ai helper: upload a local image, create a job, poll it, download the result.

Key comes from the KIE_API_KEY environment variable (never stored in the repo).
Errors from kie.ai arrive as HTTP 200 with a non-200 `code` in the body, so check `code`.
"""
import base64
import json
import mimetypes
import os
import time
import urllib.request

API = "https://api.kie.ai"
UPLOAD = "https://kieai.redpandaai.co/api/file-base64-upload"


def _key():
    k = os.environ.get("KIE_API_KEY")
    if not k:
        raise SystemExit("Set KIE_API_KEY in the environment")
    return k


def _call(url, body=None, method=None, headers=None):
    h = {"Authorization": f"Bearer {_key()}", "Content-Type": "application/json"}
    h.update(headers or {})
    data = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request(url, data=data, headers=h, method=method or ("POST" if data else "GET"))
    with urllib.request.urlopen(req, timeout=120) as r:
        return json.loads(r.read().decode())


def upload(path, folder="ninu"):
    mime = mimetypes.guess_type(path)[0] or "image/png"
    b64 = base64.b64encode(open(path, "rb").read()).decode()
    res = _call(UPLOAD, {"base64Data": f"data:{mime};base64,{b64}", "uploadPath": folder, "fileName": os.path.basename(path)})
    if res.get("code") != 200:
        raise RuntimeError(f"upload failed: {res}")
    return res["data"]["downloadUrl"]


def credits():
    return _call(f"{API}/api/v1/chat/credit")["data"]


def create(model, inp):
    res = _call(f"{API}/api/v1/jobs/createTask", {"model": model, "input": inp})
    if res.get("code") != 200:
        raise RuntimeError(f"createTask failed: {res}")
    return res["data"]["taskId"]


def wait(task_id, every=10, timeout=1500):
    t0 = time.time()
    while time.time() - t0 < timeout:
        res = _call(f"{API}/api/v1/jobs/recordInfo?taskId={task_id}")
        d = res.get("data") or {}
        state = d.get("state")
        if state == "success":
            return d
        if state == "fail":
            raise RuntimeError(f"task {task_id} failed: {d.get('failMsg') or d}")
        time.sleep(every)
    raise TimeoutError(task_id)


def result_urls(d):
    rj = d.get("resultJson")
    rj = json.loads(rj) if isinstance(rj, str) else (rj or {})
    return rj.get("resultUrls") or rj.get("result_urls") or []


def download(url, dest):
    urllib.request.urlretrieve(url, dest)
    return dest
