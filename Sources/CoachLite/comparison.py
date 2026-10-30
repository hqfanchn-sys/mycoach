"""Evidence-only comparison, guarded by the reference metadata contract."""
from reference import Lap, References
from telemetry import Recording, segment


def compare_segment(current: Recording, reference: Recording,
                    current_lap: Lap, reference_lap: Lap,
                    start_m: float, end_m: float):
    if current_lap.id == reference_lap.id:
        raise ValueError("A lap cannot be compared with itself")
    if not current_lap.usable or not References.compatible(
            reference_lap, current_lap.session, current_lap.car,
            current_lap.layout, current_lap.conditions):
        raise ValueError("Lap metadata does not permit a reliable comparison")
    left = segment(current, start_m, end_m)
    right = segment(reference, start_m, end_m)
    metrics = ("minimum_observed_speed_kmh", "maximum_observed_speed_kmh")
    return {
        "current_lap_id": current_lap.id,
        "reference_lap_id": reference_lap.id,
        "car": current_lap.car, "layout": current_lap.layout,
        "conditions": current_lap.conditions,
        "current": left, "reference": right,
        "delta_current_minus_reference": {
            key: left[key] - right[key]
            if left[key] is not None and right[key] is not None else None
            for key in metrics
        },
        "limitations": ["Sample extrema depend on sampling resolution.",
                        "This difference does not establish a cause or an optimal input."],
        "driving_advice": None,
    }
