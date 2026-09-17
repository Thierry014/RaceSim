"""Pure data objects the engine operates on. No Django, no I/O."""

from dataclasses import dataclass, field


@dataclass()
class RiderStats:
    """A rider's abilities, decoupled from the Django ``Rider`` model.

    Only the fields the engine actually needs — keep this a minimal contract.
    """

    name: str
    form: int = 0
    breakaway: bool = False

    score_climb: int = 1
    score_wave: int = 1
    score_punch: int = 1
    score_tt: int = 1
    score_sprint: int = 1
    score_steep: int = 1

    limit_distance: float = 0
    limit_slope: float = 0

    dropped: bool = False
    form: int = 1

    @property
    def limit(self) -> float:
        return self.limit_distance * self.limit_slope ** 2

@dataclass(frozen=True)
class KeyPoint:
    """One decisive segment of the course.

    Built from a ``course.key_point`` triple, e.g. ``[10, 10, 12]``.
    TODO: confirm the real meaning/units of the three numbers and rename.
    """

    distance_km: float   # where on the course this segment sits
    slope_pct: float     # gradient of the segment
    position_km: float      # how long the segment is
    progress: float

@dataclass
class Prediction:
    """The engine's result."""

    # Ordered best -> worst. Use (name, score) if you want to expose scores.
    ranking: list[tuple[str, float]] = field(default_factory=list)
    summary: str = ""

    @property
    def winner(self) -> str | None:
        return self.ranking[0][0] if self.ranking else None