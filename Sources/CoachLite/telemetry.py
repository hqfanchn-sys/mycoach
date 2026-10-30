"""Read upstream telemetry units without replacing missing channels with zero.

Official schema: Sources/Database/Libraries/TelemetryCollector.ahk.
CSV adapter explicitly supports normalized DISTANCE, seconds TIME, km/h SPEED,
and 0..1 pedals. Track length is required; units are never guessed.
"""
import csv
import hashlib
import json
import math
from dataclasses import dataclass
from pathlib import Path


def number(value):
    if value is None or value.strip().lower() in ("", "n/a", "null", "none"):
        return None
    result = float(value)
    if not math.isfinite(result):
        raise ValueError("Non-finite telemetry value")
    return result


@dataclass(frozen=True)
class Sample:
    distance_m: float
    speed_kmh: float | None
    throttle: float | None
    brake: float | None
    time_s: float | None
    tc: float | None
    abs: float | None


@dataclass(frozen=True)
class Recording:
    samples: tuple[Sample, ...]
    sha256: str
    format: str

    def summary(self):
        channels = ("speed_kmh", "throttle", "brake", "time_s", "tc", "abs")
        return {"sha256": self.sha256, "format": self.format,
                "sample_count": len(self.samples),
                "distance_start_m": self.samples[0].distance_m,
                "distance_end_m": self.samples[-1].distance_m,
                "missing": {key: sum(getattr(x, key) is None for x in self.samples)
                            for key in channels},
                "elapsed_s": (self.samples[-1].time_s - self.samples[0].time_s
                              if all(x.time_s is not None for x in self.samples) else None),
                "valid_lap": "not_verified",
                "coaching_ready": False}


def read(path, format="official", track_length_m=None):
    return read_bytes(Path(path).read_bytes(), format, track_length_m)


def read_bytes(raw, format="official", track_length_m=None):
    """Parse the exact bytes that will be retained with the lap metadata."""
    lines = raw.decode("utf-8-sig").splitlines()
    samples = []
    if format == "csv-fraction-v1":
        if track_length_m is None or not math.isfinite(track_length_m) or track_length_m <= 0:
            raise ValueError("A verified track length in meters is required")
        reader = csv.DictReader(lines)
        required = {"DISTANCE", "TIME", "SPEED", "THROTTLE", "BRAKE"}
        if not required.issubset(reader.fieldnames or []):
            raise ValueError("Missing required CSV headers")
        rows = ((i, [r["DISTANCE"], r["THROTTLE"], r["BRAKE"],
                      "", "", "", r["SPEED"], r.get("TC"), r.get("ABS"),
                      "", "", "", "", r["TIME"]]) for i, r in enumerate(reader, 2))
    elif format == "official":
        rows = enumerate(csv.reader(lines, delimiter=";"), 1)
    else:
        raise ValueError("Unsupported format")
    last_time = None
    for line, row in rows:
        if not row:
            continue
        try:
            if len(row) < 14:
                raise ValueError("At least 14 official columns are required")
            d, throttle, brake, speed, tc, abs_value = [number(row[i]) for i in (0, 1, 2, 6, 7, 8)]
            if d is None or d < 0:
                raise ValueError("Distance must be present and nonnegative")
            if format == "csv-fraction-v1":
                if d > 1:
                    raise ValueError("Normalized distance must be in 0..1")
                d *= track_length_m
            time = number(row[13])
            if time is not None and format == "official":
                time /= 1000
            for pedal in (throttle, brake):
                if pedal is not None and not 0 <= pedal <= 1:
                    raise ValueError("Pedal value outside 0..1")
            if speed is not None and speed < 0:
                raise ValueError("Negative speed")
            if samples and d < samples[-1].distance_m:
                raise ValueError("Distance reset: split into laps before import")
            if time is not None:
                if time < 0 or (last_time is not None and time < last_time):
                    raise ValueError("Time reset or negative time")
                last_time = time
            samples.append(Sample(d, speed, throttle, brake, time, tc, abs_value))
        except (ValueError, TypeError) as exc:
            raise ValueError(f"Line {line}: {exc}") from None
    if len(samples) < 2 or samples[-1].distance_m <= samples[0].distance_m:
        raise ValueError("Recording needs at least two samples covering positive distance")
    return Recording(tuple(samples), hashlib.sha256(raw).hexdigest(), format)


def segment(recording, start_m, end_m):
    """Observed samples, not optimal braking advice or exact segment timing."""
    if not math.isfinite(start_m) or not math.isfinite(end_m) or start_m >= end_m:
        raise ValueError("Invalid segment interval")
    if start_m < recording.samples[0].distance_m or end_m > recording.samples[-1].distance_m:
        raise ValueError("Segment is outside recorded coverage")
    selected = [s for s in recording.samples if start_m <= s.distance_m <= end_m]
    if len(selected) < 2:
        raise ValueError("Insufficient segment samples")
    speeds = [s.speed_kmh for s in selected]
    return {"source_sha256": recording.sha256, "requested_start_m": start_m,
            "requested_end_m": end_m, "observed_start_m": selected[0].distance_m,
            "observed_end_m": selected[-1].distance_m, "samples": len(selected),
            "minimum_observed_speed_kmh": min(speeds) if None not in speeds else None,
            "maximum_observed_speed_kmh": max(speeds) if None not in speeds else None,
            "exact_segment_time_s": None,
            "note": "Sample extrema only; no causal diagnosis or driving instruction."}


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Inspect official or explicit normalized telemetry")
    parser.add_argument("file")
    parser.add_argument("--format", choices=("official", "csv-fraction-v1"), default="official")
    parser.add_argument("--track-length-m", type=float)
    parser.add_argument("--output")
    args = parser.parse_args()
    try:
        result = read(args.file, args.format, args.track_length_m).summary()
    except (ValueError, OSError, UnicodeError) as exc:
        parser.exit(2, f"Import failed: {exc}\n")
    report = json.dumps(result, ensure_ascii=False, indent=2)
    if args.output:
        with Path(args.output).open("x", encoding="utf-8") as output:
            output.write(report + "\n")
    else:
        print(report)
