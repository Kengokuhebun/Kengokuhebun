import sys, subprocess, numpy as np, cv2, mediapipe as mp
from mediapipe.tasks import python as mpt
from mediapipe.tasks.python import vision
opts = vision.ImageSegmenterOptions(base_options=mpt.BaseOptions(model_asset_path="selfie_multiclass.tflite"),
                                    running_mode=vision.RunningMode.VIDEO, output_confidence_masks=True)
for name in sys.argv[1:]:
    src = f"../ugc/video/{name}.mp4"
    cap = cv2.VideoCapture(src); fps = cap.get(cv2.CAP_PROP_FPS)
    w, h = int(cap.get(3)), int(cap.get(4))
    out = subprocess.Popen(["ffmpeg","-v","error","-y","-f","rawvideo","-pix_fmt","gray","-s",f"{w}x{h}","-r",str(fps),"-i","-",
                            "-c:v","libx264","-crf","12","-pix_fmt","yuv420p",f"mask_{name}.mp4"], stdin=subprocess.PIPE)
    prev = None; i = 0
    with vision.ImageSegmenter.create_from_options(opts) as seg:
        while True:
            ok, frame = cap.read()
            if not ok: break
            img = mp.Image(image_format=mp.ImageFormat.SRGB, data=cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            res = seg.segment_for_video(img, int(i * 1000 / fps))
            person = 1.0 - res.confidence_masks[0].numpy_view().astype(np.float32)  # index 0 = background
            person = cv2.resize(person, (w, h), interpolation=cv2.INTER_LINEAR)
            prev = person if prev is None else 0.6 * person + 0.4 * prev        # temporal smoothing
            m = np.clip((prev - 0.35) / 0.3, 0, 1)                              # firm edges
            m = cv2.GaussianBlur(m, (0, 0), 1.6)                                 # soft feather
            out.stdin.write((m * 255).astype(np.uint8).tobytes()); i += 1
    out.stdin.close(); out.wait(); print(name, i, "frames", flush=True)
