"""R9b: generate the shots for the sung 3D cartoon ad with Seedance 2.0 Mini on kie.ai.

Usage: KIE_API_KEY=... WORK=/path/to/workdir python3 build-r9b-sung-ad.py gen
WORK must contain assets/maya_ref.png, assets/product_master.jpg (clips are written to WORK/clips).
Shot timings follow the generated song (word timestamps): see SHOTS "at" fields (seconds in the final cut).
"""
import json
import os
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import kie_pipeline as k  # noqa: E402

WORK = os.environ.get("WORK", ".")
CLIPS = f"{WORK}/clips"
os.makedirs(CLIPS, exist_ok=True)

STYLE = ("3D cartoon, soft Pixar-style animation, large expressive eyes, rounded friendly shapes, soft subsurface skin scattering, "
         "tactile materials, shallow depth of field, gentle film-like lighting, vertical 9:16. No text, no letters, no logos, no subtitles, "
         "no baby visible, no extra fingers, no duplicate characters. ")
DISP = (" The dispenser must look exactly like the product in the reference image: cream scalloped dome cap on top, clear cylinder of golden oil "
        "with fine 1-4ml measurement marks, and a cluster of hollow translucent silicone tips at the base.")
MAYA_PAST = "Maya from reference image 1, no bonnet, wavy dark hair, oatmeal knit cardigan, no towel"

# id, final-cut start/end (s), generated duration (s), resolution, reference keys, prompt
SHOTS = [
    dict(id="B1", at=(13.3, 18.15), dur=5, res="480p", refs=[], prompt=(
        "A paper wall calendar with a blank grid hangs above a wooden bathroom shelf in cool desaturated blue light. A gold marker draws a hand-drawn "
        "circle around one square in the Sunday column. The page flips to a new week while a small amber glass bottle on the shelf slowly slides "
        "backward, stop-motion style. No readable text or numbers, plain blank grid. Static locked camera, slow rack focus from the calendar down to the shelf. Quiet, heavy mood.")),
    dict(id="B2", at=(18.15, 26.75), dur=9, res="480p", refs=[], first_from="B1", prompt=(
        "Continue in the same cool desaturated blue light. The page flips again, the gold marker circles the Sunday square again with no check mark, "
        "the page flips once more and the Sunday square stays empty, while the small amber glass bottle slides further back along the shelf until it is "
        "hidden behind other plain bottles. A long still pause at the end. Static locked camera, slow rack focus. No readable text, blank grid. Resigned mood.")),
    dict(id="C1", at=(26.75, 32.75), dur=6, res="720p", refs=["maya", "product"], prompt=(
        f"{MAYA_PAST}, sits cross-legged on a cream bed at night. The room starts in cool blue light, a bedside lamp clicks on and the room warms to soft amber. "
        "She opens a plain cream gift box on the bed, lifts out the small oil dispenser shown in reference image 2 and holds it up, the hollow translucent tips "
        "catching the warm light, a spark of hope in her eyes. Slow push-in from a medium shot to a close-up of the tips." + DISP)),
    dict(id="D1", at=(32.75, 36.35), dur=4, res="480p", refs=["maya", "product"], prompt=(
        f"{MAYA_PAST}, in warm amber bedroom light, parts her hair down the center with the fingers of one hand and raises the oil dispenser from reference "
        "image 2 in her other hand above the part, calm and curious. Medium close-up from slightly above, locked camera, slow push-in." + DISP)),
    dict(id="D2", at=(36.35, 40.2), dur=4, res="720p", refs=["product"], prompt=(
        "Stylized soft cartoon 3D cross-section close-up of a scalp, side-on macro: soft rounded cylindrical dark hair strands, a clean center part, the dispenser "
        "from the reference image lowers so its hollow translucent silicone tips pass between the strands and touch the skin, a golden oil droplet slowly "
        "releases from the tips and spreads across the skin with a soft warm glow. Warm amber lighting, gentle and clean, cartoonish, not anatomical." + DISP)),
    dict(id="D3", at=(40.2, 45.4), dur=6, res="480p", refs=["maya", "product"], prompt=(
        f"{MAYA_PAST}, in warm amber light, presses the tips of the oil dispenser from reference image 2 against her scalp along her center part with one hand, "
        "then slides it slowly along the part. Her shoulders and the sheets stay clean and dry. Calm, satisfied expression. Medium shot, locked camera, slow push-in." + DISP)),
    dict(id="E1", at=(45.4, 49.5), dur=5, res="480p", refs=["maya", "product"], prompt=(
        f"Night one. {MAYA_PAST}, sits on the edge of a bed in cool desaturated blue moonlight, presses the oil dispenser from reference image 2 against her scalp "
        "along the part with her eyes closed, hopeful and uncertain. Medium close-up, slow push-in, shallow depth of field." + DISP)),
    dict(id="E2", at=(49.5, 59.7), dur=10, res="480p", refs=["maya", "product"], prompt=(
        f"{MAYA_PAST}, eyes closed, holds the oil dispenser from reference image 2 against her scalp. Over the shot the room light gradually shifts from cool blue "
        "to warm amber, her shoulders drop, she opens her eyes with gentle surprise and a soft genuine smile, lowers the dispenser into her lap and exhales. "
        "Medium close-up, slow push-in, shallow depth of field, tender relief." + DISP)),
    dict(id="F1", at=(59.7, 64.6), dur=5, res="480p", refs=["product"], prompt=(
        "Wide shot of a bedside nightstand in warm amber lamp light: the small oil dispenser from the reference image stands upright beside a folded caramel satin "
        "bonnet, a quiet white baby monitor with a steady green light, and a small digital clock showing 10:00. Dust motes drift in the lamp light. "
        "Locked camera, very slow push-in, peaceful and resolved." + DISP)),
    dict(id="F2", at=(64.6, 77.6), dur=13, res="480p", refs=["maya", "product"], prompt=(
        "Warm amber bedroom. A woman's hand in a tan robe sleeve (Maya from reference image 1) reaches to the nightstand and picks up the oil dispenser from "
        "reference image 2 without looking, as automatically as reaching for a toothbrush. The camera slowly pulls back to reveal Maya in a tan robe and caramel "
        "satin bonnet already settled on the cream bed with a faint contented smile. Peaceful, resolved mood. Slow pull-back from a close shot of the nightstand "
        "to a medium-wide shot." + DISP)),
    dict(id="G1", at=(77.6, 85.0), dur=8, res="720p", refs=["product"], prompt=(
        "On a clean cream seamless background with a thin gold horizontal line, three items float in and settle gently into a neat arrangement: the small oil "
        "dispenser from the reference image in the center, a 60ml amber glass oil bottle with a plain blank cream label on the left, and a folded caramel satin sleep "
        "bonnet on the right. A soft warm light sweeps slowly across them. Slow push-in, calm premium look, no text." + DISP)),
]


def last_frame_png(mp4, png):
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-sseof", "-0.1", "-i", mp4, "-frames:v", "1", png], check=True)
    return png


def submit(shot, refs):
    inp = {"prompt": STYLE + shot["prompt"], "generate_audio": False, "resolution": shot["res"], "aspect_ratio": "9:16",
           "duration": shot["dur"], "nsfw_checker": False}
    if shot.get("first_frame"):
        inp["first_frame_url"] = shot["first_frame"]
    elif shot["refs"]:
        inp["reference_image_urls"] = [refs[r] for r in shot["refs"]]
    return k.create("bytedance/seedance-2-mini", inp)


def gen(only=None):
    refs = json.load(open(f"{WORK}/ref_urls.json"))
    costs = json.load(open(f"{CLIPS}/costs.json")) if os.path.exists(f"{CLIPS}/costs.json") else {}
    todo = [s for s in SHOTS if (not only or s["id"] in only) and not os.path.exists(f"{CLIPS}/{s['id']}.mp4")]
    tasks = {}
    for s in todo:
        if s.get("first_from"):
            continue
        tasks[s["id"]] = submit(s, refs)
        print("submitted", s["id"], tasks[s["id"]], flush=True)

    def finish(sid):
        d = k.wait(tasks[sid], every=8)
        k.download(k.result_urls(d)[0], f"{CLIPS}/{sid}.mp4")
        costs[sid] = d.get("creditsConsumed")
        json.dump(costs, open(f"{CLIPS}/costs.json", "w"))
        print("done", sid, "credits", d.get("creditsConsumed"), flush=True)

    for s in todo:
        if s["id"] in tasks:
            try:
                finish(s["id"])
            except Exception as e:  # keep going, report at the end
                print("FAILED", s["id"], e, flush=True)
    for s in todo:
        if s.get("first_from") and os.path.exists(f"{CLIPS}/{s['first_from']}.mp4"):
            png = last_frame_png(f"{CLIPS}/{s['first_from']}.mp4", f"{WORK}/assets/{s['id']}_first.png")
            s["first_frame"] = k.upload(png)
            tasks[s["id"]] = submit(s, refs)
            print("submitted", s["id"], tasks[s["id"]], flush=True)
            try:
                finish(s["id"])
            except Exception as e:
                print("FAILED", s["id"], e, flush=True)
    print("credits left:", k.credits())


if __name__ == "__main__":
    if sys.argv[1] == "gen":
        gen(set(sys.argv[2:]) or None)
