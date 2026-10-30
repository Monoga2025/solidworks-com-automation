from faster_whisper import WhisperModel
from pathlib import Path
import argparse, json

parser = argparse.ArgumentParser()
parser.add_argument("input")
parser.add_argument("output_stem")
args = parser.parse_args()
source = Path(args.input)
out_stem = Path(args.output_stem)
out_stem.parent.mkdir(parents=True, exist_ok=True)

model = WhisperModel("small", device="cpu", compute_type="int8", local_files_only=True)
segments, info = model.transcribe(str(source), language="es", beam_size=5, vad_filter=True, word_timestamps=True)
segments = list(segments)

def stamp(seconds: float) -> str:
    ms = int(round(seconds * 1000)); h, ms = divmod(ms, 3600000); m, ms = divmod(ms, 60000); s, ms = divmod(ms, 1000)
    return f"{h:02d}:{m:02d}:{s:02d}.{ms:03d}"

payload = {"source": str(source), "language": info.language, "language_probability": info.language_probability, "duration": info.duration,
           "segments": [{"start": s.start, "end": s.end, "text": s.text.strip(),
                         "words": [{"start": w.start, "end": w.end, "word": w.word, "probability": w.probability} for w in (s.words or [])]}
                        for s in segments]}
out_stem.with_suffix(".json").write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
with out_stem.with_suffix(".vtt").open("w", encoding="utf-8") as f:
    f.write("WEBVTT\n\n")
    for i, s in enumerate(segments, 1): f.write(f"{i}\n{stamp(s.start)} --> {stamp(s.end)}\n{s.text.strip()}\n\n")
print(json.dumps({"source": str(source), "duration": info.duration, "segments": len(segments), "language": info.language}, ensure_ascii=False))
