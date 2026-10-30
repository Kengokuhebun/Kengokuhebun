"""R11: generate the new shots for the v2 sung 3D ad (hook-first, problem-mechanism block, avatar cues).

Usage: KIE_API_KEY=... WORK=/path/to/workdir python3 build-r11-v2-shots.py phase1 | bottle <clip> <sec> | phase2
WORK needs ref_urls.json (maya, product, bonnet), assets/, and clips/ from R9b (B1, C1, D1-D3, E1, E2, F2 are reused).
New clips are written to WORK/clips2. Phase 2 shots use the talking-bottle reference cut from the phase 1 bottle shot.
Shot windows are in song time (take 0 trimmed by 1.5s), see build-r11-assemble.py.
"""
import json
import os
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import kie_pipeline as k  # noqa: E402

WORK = os.environ.get("WORK", ".")
CLIPS = f"{WORK}/clips2"
os.makedirs(CLIPS, exist_ok=True)

STYLE = ("3D cartoon, soft Pixar-style animation, large expressive eyes, rounded friendly shapes, soft subsurface skin scattering, "
         "tactile materials, shallow depth of field, gentle film-like lighting, vertical 9:16. No text, no letters, no logos, no subtitles, "
         "no baby visible, no extra fingers, no duplicate characters. ")
MAYA = "Maya from reference image 1 (wavy dark hair, oatmeal knit cardigan, no bonnet)"
BOTTLE = ("a small amber glass dropper bottle with a plain blank cream label, big expressive cartoon eyes, a small mouth and tiny arms")

# id, window in song time, generated seconds, resolution, reference keys, prompt
PHASE1 = [
    dict(id="H1", at=(0.0, 3.4), dur=4, res="720p", refs=["maya"], prompt=(
        f"Tight close-up in a bathroom, cool desaturated blue light. {MAYA}, a towel over her shoulders, her hair flat, clumpy and glossy with oil, a golden oil streak "
        "running down her neck into the towel. She looks straight into the camera as if it were the mirror, eyes wide with dismay, brows pinched up, lips pressed "
        "together, then lifts a hand to touch her hairline and flinches. Locked camera with a very slight push-in. Tense and embarrassed.")),
    dict(id="H2", at=(3.4, 9.2), dur=6, res="720p", refs=[], prompt=(
        f"A wooden bathroom shelf in cool blue light with a few plain blank bottles in front. Behind them {BOTTLE} pops up from behind the front bottles, waves a tiny arm "
        "and talks cheerfully to the camera, then looks sheepish, scratches its head, a puff of dust falls off its shoulders and it shrugs apologetically. "
        "Locked camera with a slight push-in, cheeky comic mood. No readable text.")),
    dict(id="BL1", at=(9.2, 10.7), dur=4, res="480p", refs=["maya"], prompt=(
        f"{MAYA}, slumped in a rocking chair in a dark nursery at night, lit only by the amber glow of a white baby monitor on a small table beside her, rubbing her tired eyes. "
        "No baby visible. Medium close-up, slight push-in, cool blue night light, exhausted mood.")),
    dict(id="BL2", at=(10.7, 12.6), dur=4, res="480p", refs=["maya"], prompt=(
        f"{MAYA}, in a steamy bathroom with a towel on her shoulders, holds up a shampoo bottle with no readable label, frowns at it in disbelief, then drops it into a basket "
        "with a clatter. Medium close-up, locked camera, cool desaturated blue light.")),
    dict(id="BL3", at=(12.6, 14.4), dur=4, res="480p", refs=["maya"], prompt=(
        f"{MAYA}, with a towel on her shoulders, sits on the edge of a bathtub, shoulders slumped, rests her forehead in her palm and lets out a small guilty exhale. "
        "Medium close-up, locked camera, cool desaturated blue light.")),
    dict(id="R2", at=(19.9, 22.0), dur=4, res="720p", refs=[], prompt=(
        "Stylized soft cartoon 3D cross-section, side-on macro: rounded cylindrical dark hair strands standing on a clean pale skin surface. Golden oil drips from a glass "
        "dropper above and lands on the TOP of the strands, coating them and sliding down their sides, while the bare skin between the strands at the bottom stays clean and dry, "
        "with a visible gap of air between the oil and the skin. Cool blue lighting, gentle and cartoonish, not anatomical. No text.")),
    dict(id="R3", at=(22.0, 26.2), dur=6, res="480p", refs=["maya"], prompt=(
        f"{MAYA}, seen from behind and the side with a towel over her shoulders: a glossy golden oil streak slowly runs down the back of her neck and soaks into the towel, "
        "the towel darkening, her head drooping. Medium close-up, slow push-in, cool blue light, heavy mood.")),
    dict(id="P2", at=(29.9, 32.1), dur=4, res="480p", refs=[], prompt=(
        "Macro: a glass dropper pipette with a black rubber bulb hovers in a cool blue spotlight, a fat golden drop swells at its tip and falls in slow motion onto a strand "
        "of dark hair, splashing and sliding off the side. Locked camera, cool blue light, cartoonish.")),
    dict(id="P3", at=(32.1, 34.35), dur=4, res="480p", refs=[], prompt=(
        "Stylized soft cartoon 3D cross-section macro: round dark hair strands with golden oil beads sitting on them and sliding off sideways like water off a waxy leaf; then the camera "
        "tilts down to clean bare skin where a single golden droplet lands, spreads and is absorbed with a soft warm glow. Gentle, cartoonish, not anatomical, no text.")),
    dict(id="G2", at=(61.8, 68.8), dur=8, res="720p", refs=["product", "bonnet"], prompt=(
        "On a clean cream seamless background with a thin gold horizontal line, two items glide in and rest on a soft cream surface side by side with clear space between them: "
        "on the left the small oil dispenser from reference image 1; on the right a caramel satin HAIR bonnet like reference image 2, a soft round puffy cap shape (a hair bonnet, "
        "NOT an eye mask, NOT a nightcap, no head, no face). Only these two items, no bottles. A soft warm light sweeps slowly across them. Slow push-in, calm premium look, no text. "
        "The dispenser must look exactly like reference image 1: cream scalloped dome cap on top, clear cylinder of golden oil with fine 1-4ml measurement marks, and a cluster of "
        "hollow translucent silicone tips at the base.")),
]
# these use the talking-bottle reference ("bottle") cut from H2
PHASE2 = [
    dict(id="K1", at=(58.4, 61.8), dur=4, res="480p", refs=["bottle"], prompt=(
        "The whole scene is warm golden-amber, a cream wall and a honey-colored wooden shelf in soft golden lamp glow, no blue tones at all. A paper wall calendar with a plain blank grid hangs above the shelf. Along one horizontal row of seven squares, small gold check marks pop on "
        "one after another across the first six squares and the seventh square stays bare and blank. On the shelf below, the small amber dropper bottle with big cartoon eyes from "
        "reference image 1 waves goodbye with a tiny arm and slides out of frame. Static locked camera. No readable numbers or text.")),
    dict(id="R1", at=(17.4, 19.9), dur=4, res="480p", refs=["bottle"], prompt=(
        "The same wooden shelf in cool blue light. The small amber dropper bottle with big cartoon eyes from reference image 1 hops to the front of the shelf, glances left and right, "
        "then leans toward the camera conspiratorially and waves a tiny arm as if to say come closer. Slow push-in, cheeky mood. No text.")),
    dict(id="P1", at=(26.2, 29.9), dur=5, res="480p", refs=["maya", "bottle"], prompt=(
        "Maya from reference image 1 with bare wavy dark hair (NO bonnet, NO hat, NO head covering), a white towel on her shoulders, leans on a bathroom counter in cool blue light. "
        "On the counter beside her stands the small amber dropper bottle character from reference image 2 with big cartoon eyes, a small mouth and tiny arms; it reaches out and gently "
        "pats her finger. Her expression softens from tension to relief, a long exhale, her shoulders drop. Medium close-up, slow push-in, tender mood.")),
    dict(id="M1", at=(53.0, 58.4), dur=6, res="720p", refs=["maya", "bottle"], prompt=(
        "Tight close-up as in a bathroom mirror, now in warm amber light. Maya from reference image 1 in a caramel satin bonnet and tan robe, hair neat, no towel, smiles at the camera "
        "with a raised eyebrow of triumph and a small playful head shake; behind her on a shelf the small amber bottle with cartoon eyes from reference image 2 shrugs sheepishly. "
        "Locked camera with a slow push-in. Warm, triumphant, playful.")),
]


def submit(shot, refs):
    inp = {"prompt": STYLE + shot["prompt"], "generate_audio": False, "resolution": shot["res"], "aspect_ratio": "9:16",
           "duration": shot["dur"], "nsfw_checker": False}
    if shot["refs"]:
        inp["reference_image_urls"] = [refs[r] for r in shot["refs"]]
    return k.create("bytedance/seedance-2-mini", inp)


def gen(shots, only=None):
    refs = json.load(open(f"{WORK}/ref_urls.json"))
    cpath = f"{CLIPS}/costs.json"
    costs = json.load(open(cpath)) if os.path.exists(cpath) else {}
    todo = [s for s in shots if (not only or s["id"] in only) and not os.path.exists(f"{CLIPS}/{s['id']}.mp4")]
    tasks = {}
    for s in todo:
        tasks[s["id"]] = submit(s, refs)
        print("submitted", s["id"], tasks[s["id"]], flush=True)
    for s in todo:
        try:
            d = k.wait(tasks[s["id"]], every=8)
            k.download(k.result_urls(d)[0], f"{CLIPS}/{s['id']}.mp4")
            costs[s["id"]] = d.get("creditsConsumed")
            json.dump(costs, open(cpath, "w"))
            print("done", s["id"], "credits", d.get("creditsConsumed"), flush=True)
        except Exception as e:
            print("FAILED", s["id"], e, flush=True)
    print("credits left:", k.credits())


def bottle(clip, sec):
    png = f"{WORK}/assets/bottle_ref.png"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", str(sec), "-i", f"{CLIPS}/{clip}.mp4", "-frames:v", "1", png], check=True)
    refs = json.load(open(f"{WORK}/ref_urls.json"))
    refs["bottle"] = k.upload(png)
    json.dump(refs, open(f"{WORK}/ref_urls.json", "w"))
    print("bottle ref", refs["bottle"])


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "phase1":
        gen(PHASE1, set(sys.argv[2:]) or None)
    elif cmd == "phase2":
        gen(PHASE2, set(sys.argv[2:]) or None)
    elif cmd == "bottle":
        bottle(sys.argv[2], sys.argv[3])
