# CoachLite development modules

These modules live in the pinned official Simulator Controller 7.3.2 source tree.
They are not yet connected to the live collector, GUI, Sol or Live audio.

Run tests from this directory: `python -m unittest discover -v`.

## Import inspection

Official `.telemetry` files: `python telemetry.py lap.telemetry`.
The first 14 semicolon-separated fields follow the upstream TelemetryCollector
schema. This initial reader requires numeric millisecond timestamps or explicit
missing values; formatted clock timestamps are not yet supported.

Explicit CSV format: `python telemetry.py reference.csv --format csv-fraction-v1 --track-length-m 24154.4`.

This CSV contract requires DISTANCE in 0..1 lap fraction, TIME in seconds, SPEED
in km/h and THROTTLE/BRAKE in 0..1. Optional TC/ABS stay missing when absent.
Length must come from verified layout metadata, never a filename or a guess.
Use `--output new-report.json` to write an inspection report without overwriting
an existing file. Import inspection does not certify lap validity, metadata
compatibility, map readiness or professional reference quality.

## Reference and comparison

`References` consumes validated `Lap` metadata. IDs must identify immutable laps.
Unknown conditions are conservatively excluded until condition handling is
implemented. Manual selection affects the next lap and is not silently replaced.

`compare_segment` checks metadata compatibility and emits observed speed extrema,
signed differences and source checksums. It does not claim exact boundary timing,
infer the cause of a difference, or generate driving advice. Callers must associate
metadata with the correct recording; persistence and collector binding remain TODO.
# Persistent pipeline

`storage.Archive(path)` opens a local SQLite archive. `pipeline.Pipeline(archive)`
restores recorded laps and the pinned reference, but deliberately discards any
in-flight lap from a previous process. Call `archive.close()` on shutdown.

The collector adapter must supply trustworthy `Lap` metadata. Call `begin` at
lap start, then `finish` with the completed file. `finish_official` accepts the
upstream `Lap N.telemetry` naming convention; it is not a live watcher. Session
identity and validity cannot be inferred from filenames. Never feed an old
directory's files as if they belonged to the new session.

`import_reference` archives external data without pinning it or upgrading its
validity. `select` takes effect next lap. `compare` uses the reference ID saved
at that lap's start and loads both byte streams from the archive. Original
source file changes therefore cannot silently alter historical comparisons.

Raw bytes, units and metadata are saved in one transaction. Parsing failure
leaves the active lap available for retry. This is a single-process local
component, not yet wired to AHK, iRacing session events, Sol or Live. Conditions
remain an exact explicit compatibility key; production condition derivation
and lap validity checks are pending.

