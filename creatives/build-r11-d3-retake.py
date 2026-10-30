"""R11: retake of shot D3 ("directly on the skin") with the dispenser held upright.
The R9b take held it tilted on its side, which no longer read as the product.

Usage: KIE_API_KEY=... WORK=/path/to/workdir python3 build-r11-d3-retake.py
Writes WORK/clips2/D3b.mp4 and D3c.mp4 (two takes, pick the better one).
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import kie_pipeline as k  # noqa: E402

WORK = os.environ.get("WORK", ".")
STYLE = ("3D cartoon, soft Pixar-style animation, large expressive eyes, rounded friendly shapes, soft subsurface skin scattering, "
         "tactile materials, shallow depth of field, gentle film-like lighting, vertical 9:16. No text, no letters, no logos, no subtitles, "
         "no baby visible, no extra fingers, no duplicate characters. ")
DISP = (" The dispenser must look exactly like the product in reference image 2: a palm-sized upright cylinder with a cream scalloped dome cap on top, "
        "a clear cylinder of golden oil with fine 1-4ml measurement marks, and a cluster of hollow translucent silicone tips at the base. "
        "It is always held perfectly VERTICAL, cap pointing straight up, tips pointing straight down, never tilted, never on its side, cap never removed.")
BASE = ("Maya from reference image 1 (wavy dark hair, oatmeal knit cardigan, no bonnet), sits upright against a tufted headboard in warm amber lamp light, eyes closed, "
        "holds the oil dispenser from reference image 2 upright in one hand with the tips resting against her scalp along her center part, ")
TAKES = {
    "D3b": BASE + "then slowly slides it a short way along the part, content and calm, shoulders and sheets clean and dry. Medium close-up, locked camera, slow push-in." + DISP,
    "D3c": BASE + "her free hand lifted to part her hair beside the tips, a soft satisfied smile. The hand holding the dispenser stays still and the dispenser stays vertical. "
          "Medium close-up, locked camera, very slow push-in." + DISP,
}


def main():
    refs = json.load(open(f"{WORK}/ref_urls.json"))
    tasks = {}
    for tid, prompt in TAKES.items():
        tasks[tid] = k.create("bytedance/seedance-2-mini", {
            "prompt": STYLE + prompt, "generate_audio": False, "resolution": "720p", "aspect_ratio": "9:16",
            "duration": 4, "nsfw_checker": False, "reference_image_urls": [refs["maya"], refs["product"]]})
        print("submitted", tid, tasks[tid], flush=True)
    for tid, t in tasks.items():
        d = k.wait(t, every=8)
        k.download(k.result_urls(d)[0], f"{WORK}/clips2/{tid}.mp4")
        print("done", tid, d.get("creditsConsumed"), flush=True)
    print("credits left:", k.credits())


if __name__ == "__main__":
    main()
