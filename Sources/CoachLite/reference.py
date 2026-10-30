"""Reference selection for the simplified coach; no network or model calls.

The original collector remains responsible for obtaining telemetry. This module
accepts validated lap metadata and freezes a reference for each new lap.
"""
from dataclasses import dataclass
from math import isfinite


@dataclass(frozen=True)
class Lap:
    id: str
    session: str
    car: str
    layout: str
    conditions: str | None
    seconds: float
    valid: bool
    complete: bool
    source: str = "recorded"

    @property
    def usable(self) -> bool:
        return bool(self.id and self.session and self.car and self.layout
                    and self.valid and self.complete
                    and isfinite(self.seconds) and self.seconds > 0)


class References:
    def __init__(self):
        self.laps: dict[str, Lap] = {}
        self.pinned: str | None = None
        self.active: tuple[str, str, str, str, str | None] | None = None
        self.snapshot: Lap | None = None

    def add(self, lap: Lap) -> None:
        if not lap.id:
            raise ValueError("Lap ID is required")
        previous = self.laps.get(lap.id)
        if previous is not None and previous != lap:
            raise ValueError("Existing lap IDs cannot be overwritten")
        self.laps[lap.id] = lap

    def select(self, lap_id: str | None) -> None:
        """Select for the NEXT lap. None returns to automatic selection."""
        if lap_id is not None:
            if lap_id not in self.laps or not self.laps[lap_id].usable:
                raise ValueError("Selected reference is unavailable or invalid")
        self.pinned = lap_id

    @staticmethod
    def compatible(lap: Lap, session: str, car: str, layout: str,
                   conditions: str | None) -> bool:
        if not lap.usable or lap.car != car or lap.layout != layout:
            return False
        # Unknown conditions never silently qualify cross-session references.
        if conditions is None or lap.conditions is None:
            return False
        return lap.conditions == conditions

    def begin(self, lap_id: str, session: str, car: str, layout: str,
              conditions: str | None) -> Lap | None:
        identity = (lap_id, session, car, layout, conditions)
        if self.active == identity:
            return self.snapshot
        if lap_id in self.laps:
            raise ValueError("A recorded lap cannot be started again")
        candidates = [lap for lap in self.laps.values()
                      if self.compatible(lap, session, car, layout, conditions)]
        if self.pinned is not None:
            candidates = [lap for lap in candidates if lap.id == self.pinned]
        self.snapshot = min(candidates, key=lambda lap: (lap.seconds, lap.id), default=None)
        self.active = identity
        return self.snapshot

    def finish(self, lap: Lap) -> Lap | None:
        """Return the OLD reference before admitting the completed lap."""
        identity = (lap.id, lap.session, lap.car, lap.layout, lap.conditions)
        if self.active != identity:
            raise ValueError("Completion belongs to a different lap or session")
        reference = self.snapshot
        self.add(lap)
        self.active = None
        self.snapshot = None
        return reference

    def disconnect(self) -> None:
        self.active = None
        self.snapshot = None
