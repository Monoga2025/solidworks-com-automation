# SolidWorks COM Automation (C# / .NET 8)

A Windows console tool that drives SolidWorks through its official COM API to build parametric gear parts and a threaded-union checklist from a JSON profile. It started as a way to practice scripting SolidWorks for a mechanical-design course.

## What it does

- Connects to a running/licensed SolidWorks via `SolidWorks.Interop`.
- Creates a part with an **Equation Manager** table (teeth, module, pressure angle, helix angle, derived diameters).
- Builds spur/helical **gear parts**: generates the tooth outline from the gear parameters, extrudes, adds bore and keyway, and lofts a twisted profile for the helical case (`CreateTwistedGearLoft`).
- Saves each part and attempts a two-gear assembly; checks that the result is a solid body before saving.
- `--smoke-test` builds a single helical gear to verify the connection.

`tools/transcribe_local.py` is an unrelated helper: local Spanish speech-to-text (faster-whisper, WebVTT + JSON output) used to take notes from screen recordings.

## Run

Requires Windows, a licensed SolidWorks (paths in the `.csproj` point to the default install dir), and the .NET 8 SDK (x64).

```powershell
cd runner
copy profiles.example.json profiles.json   # edit values
dotnet build -c Release
dotnet run -c Release -- profiles.json [--smoke-test]
```

## Status

🟡 Experimental. COM connection, Equation Manager and basic gear geometry are automated. The final tooth profile, swept cut, circular pattern, assembly mates and real threaded geometry are intentionally left staged (the tool writes pending-notes files instead of claiming success) because selections depend on the SolidWorks version. Always review generated models by hand.

The profile fields (`StudentName`, `StudentId`) come from the original coursework use; the example file contains placeholders only.

## Folder guide

| Folder | What it holds |
|---|---|
| [runner/](runner/README.md) | C# console runner and COM controller |
| [tools/](tools/README.md) | Local transcription helper (standalone) |
| [tools/pdf-generators/](tools/pdf-generators/README.md) | Study-guide PDF generators (standalone) |
| [macros/](macros/README.md) | Earlier VBA macros, kept for reference |

---

Built by Monoga · [github.com/Monoga2025](https://github.com/Monoga2025)
