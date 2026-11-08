import json, subprocess, numpy as np
from faster_whisper import WhisperModel
m = WhisperModel("small.en", device="cpu", compute_type="int8")
out = {}
for name in ["H1","H2","H3","BODY"]:
    raw = subprocess.run(["ffmpeg","-v","error","-i",f"../ugc/video/{name}.mp4","-ac","1","-ar","16000","-f","f32le","-"],capture_output=True).stdout
    audio = np.frombuffer(raw, np.float32)
    segs, _ = m.transcribe(audio, word_timestamps=True, beam_size=5)
    out[name] = [{"w": w.word.strip(), "s": round(w.start, 3), "e": round(w.end, 3)} for s in segs for w in s.words]
    print(name, len(out[name]), round(len(audio)/16000,2), " ".join(x["w"] for x in out[name]), flush=True)
json.dump(out, open("words.json", "w"), indent=1)
