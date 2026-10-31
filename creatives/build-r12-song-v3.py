"""R12: generate the v3 song (answer front-loaded, ~50s) with Suno V6 on kie.ai and fetch word timestamps.

Usage: KIE_API_KEY=... WORK=/path/to/workdir python3 build-r12-song-v3.py
Writes WORK/song3/take{0,1}.mp3 and take{0,1}_ts.json (synchronous timestamped-lyrics response).
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import kie_pipeline as k  # noqa: E402

WORK = os.environ.get("WORK", ".")
OUT = f"{WORK}/song3"
os.makedirs(OUT, exist_ok=True)

LYRICS = """[Verse 1]
Why is my hair oil not doing anything?
Because, mama, oil poured on your hair
mostly stays on your hair.

[Pre-Chorus]
It wasn't you. It was never you.
It was the dropper.

[Verse 2]
So meet the one with hollow silicone tips.
Press them to your scalp,
and the oil releases right there.

[Bridge]
The first night, mama, I felt it. Oh.
This is what it's supposed to feel like.

[Final Chorus]
Not doing anything?
It was never getting there.

[Outro]
The Nee-noo Kit. Free U.S. shipping.
Thirty days to love it or send it back.
Make tonight the easy one.
"""

STYLE = ("Playful cartoon musical-theatre pop, 112 BPM, steady four-on-the-floor pulse, 4/4. One expressive female vocal, bright and "
         "conversational with a little attitude, clear diction, English. Light kick and snare, finger snaps and handclaps, pizzicato strings, "
         "ukulele, felt piano, a bouncy bass. The pulse is steady and never drops out. Words are sung rhythmically on the beat, one syllable per beat, "
         "phrases follow one another with small breaths. Cheeky and tense in the first verse, warm and open in the final chorus. "
         "The vocal starts immediately in the first half second with no instrumental intro and no instrumental break. "
         "Short song, about 50 seconds, resolved ending.")
NEG = "long intro, instrumental break, ballad, slow, lullaby, choir, rap, autotune, spoken word"


def main():
    tid = k.create("ai-music-api/generate", {
        "custom_mode": True, "instrumental": False, "model": "V6", "prompt": LYRICS, "style": STYLE,
        "title": "Not Doing Anything v3", "negative_tags": NEG, "vocal_gender": "f"})
    print("task", tid, flush=True)
    d = k.wait(tid, every=10, timeout=900)
    json.dump(d, open(f"{OUT}/task.json", "w"))
    res = json.loads(d["resultJson"]) if isinstance(d["resultJson"], str) else d["resultJson"]
    for i, t in enumerate(res["data"][:2]):
        k.download(t["audio_url"], f"{OUT}/take{i}.mp3")
        ts = k._call(f"{k.API}/api/v1/jobs/createTask", {"model": "ai-music-api/timeStamped-lyrics",
                                                         "input": {"task_id": tid, "audio_id": t["id"]}})
        json.dump(ts, open(f"{OUT}/take{i}_ts.json", "w"))
        print("take", i, t["id"], "duration", t.get("duration"), flush=True)
    print("credits left:", k.credits())


if __name__ == "__main__":
    main()
