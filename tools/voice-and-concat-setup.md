# VoiceStudio + Concat MCP — setup notes

Both tools are installed to work from this cloud session. Ready to use (see caveats).

## 1. VoiceStudio (voice generation + dubbing + transcription)

**Repo:** https://github.com/debpalash/VoiceStudio
**Local clone:** `/home/user/debpalash/voicestudio`
**Venv:** `/home/user/debpalash/voicestudio/.venv` (Python 3.11, CPU-only torch)
**Install method:** `uv sync --group cpu --no-group cuda --no-install-project`

### What it can do (local, no external API)
- **TTS / speech generation** — text to WAV in 646 languages, voice-clone or voice-design
- **Voice cloning** — reference audio clip → new voice profile
- **Transcription** — audio to text (WhisperX-backed)
- **Video dubbing** — translate and dub preserving timing
- **Voice design** — describe a voice in words, generate it

### MCP tools exposed (`backend/mcp_server.py`)
- `generate_speech` — text → WAV or Ogg/Opus
- `clone_voice` — reference audio (base64 or file path) → new voice profile
- `transcribe` — audio → text
- `list_voices`, `list_languages`, `list_personalities`, `check_health`
- Resources: `voice://{profile_id}`, `history://recent`

### Launch

```bash
# Stdio transport (what MCP clients use)
cd /home/user/debpalash/voicestudio
./.venv/bin/python -m backend.mcp_server

# SSE transport (if you need HTTP)
./.venv/bin/python -m backend.mcp_server --sse
```

### Environment variables to set when using
```bash
# where the MCP can read/write audio files; must be set or path-shaped args are refused
OMNIVOICE_MCP_BASE_PATH=/home/user/voicestudio-io

# how speech-generate returns audio: "resources" (base64 inline), "files" (URL), or "both"
OMNIVOICE_MCP_OUTPUT_MODE=both
```

### Caveats to know up front
- **Models download on first call.** The default TTS model (`OmniVoice`) is ~2.4 GB; it downloads from HuggingFace on the first `generate_speech` call. 5–15 min on first use, then cached locally.
- **CPU-only → slow.** Realtime is ~0.3-0.5× on CPU for the main OmniVoice model; a 30-second clip takes 60-90 seconds to synthesise. Fine for drafting ads one-off, not for high throughput.
- **GPU would be 10-20× faster** but needs a GPU runtime (not available in this sandbox).

## 2. Concat MCP (video editor automation)

**Repo:** https://github.com/AdriGeorge/concatt-mcp
**Local clone:** `/home/user/adrigeorge/concatt-mcp`
**Venv:** `/home/user/adrigeorge/concatt-mcp/.venv` (Python 3.12)
**Install method:** `pip install -r requirements.txt` (mcp 1.30.0 + python-dotenv + jsonschema)

### What it does
Thin bridge between an MCP client and the **Concat video editor's** Remote API (local TCP JSON-RPC on 127.0.0.1:7420). Exposes 22 tools covering:
- Project inspect/create/open
- Media import
- Timeline edits
- Template application
- Preview render
- Export
- Event polling

### Launch

```bash
cd /home/user/adrigeorge/concatt-mcp
./.venv/bin/python concat_mcp.py
# or
./start.sh
```

### Config (`.env` beside `concat_mcp.py`)
```
CONCAT_API_HOST=127.0.0.1
CONCAT_API_PORT=7420
CONCAT_API_TOKEN=<token from Concat Settings → Remote>
```
Placeholder `.env` is in place; real token must be pasted before any tool call will succeed.

### ⚠ IMPORTANT caveat
**The MCP is just the bridge — it does not include Concat itself.** Concat is a desktop Electron editor and does NOT run headless in this cloud sandbox. For the tools to do anything, Concat must be installed and running on a machine the MCP can reach on port 7420.

Realistic options:
- **Option A (recommended):** run Concat on your local computer, run the MCP on your local computer, use it from a Claude session on your laptop. The MCP in this cloud session is pre-configured and ready to serve as reference / for code inspection.
- **Option B:** use **ffmpeg** directly (already installed in this cloud session) for video concatenation, cuts, overlays, format conversion. No GUI needed. For straight concatenation of our swipe-based voice-over videos, ffmpeg + a few lines of shell is simpler than driving a GUI editor from here.
- **Option C:** stand up Concat in a headless Electron+xvfb container. Non-trivial and fragile.

For the Glowling ad voice-over workflow (take an existing MP4, lay a new VO track, add captions, export) **ffmpeg+assembled-shell is likely the right tool for this environment, not the Concat MCP**.

## 3. What's ready right now

| Component | Installed | Launches | Functional |
|---|---|---|---|
| VoiceStudio code | ✓ | — | — |
| VoiceStudio Python deps | ✓ (CPU torch, no CUDA) | — | — |
| VoiceStudio MCP server | ✓ | can run `python -m backend.mcp_server` | **Yes**, but first TTS call triggers a ~2.4 GB model download |
| concatt-mcp code | ✓ | — | — |
| concatt-mcp Python deps | ✓ (3 packages) | — | — |
| concatt-mcp MCP server | ✓ | can run `./.venv/bin/python concat_mcp.py` | **No** — needs Concat GUI running on port 7420 somewhere reachable |
| ffmpeg (fallback for video work) | ✓ (`/usr/bin/ffmpeg`) | — | **Yes**, fully functional for concat/cut/overlay |

## 4. Suggested workflow when you want to produce video ads

1. Record voice-over scripts as text → feed into VoiceStudio MCP → get WAVs
2. Use ffmpeg in this sandbox (or Concat MCP on your local machine) to lay the WAVs over existing video clips, add captions, export MP4
3. Upload the finished MP4 via the Meta Marketing API using the workflow in `ads/launch/launch_resume.py`

Nothing is generated yet — tools are installed and ready; nothing more happens until you ask.
