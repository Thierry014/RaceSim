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
    attack_index: int = 0

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
    position_km: float   # how long the segment is
    progress: float      # what part of the course

    @property
    def kp_cat(self) -> dict:
        kp_cat_result = {}
        progress = self.progress
        if progress > 95:
            importance = progress/100
        else:
            importance = (progress/100) ** 3
        x = progress * importance
        if self.distance_km < 3 and self.slope_pct >= 7.5 and self.progress > 95:
            kp_cat_result['steep'] = x
        if (self.distance_km < 3 and 5 < self.slope_pct < 7.5) or (self.slope_pct < 7.5 and self.progress > 95):
            kp_cat_result['punch'] = x
        if self.distance_km < 3 and self.slope_pct <= 5 and self.progress < 95:
            kp_cat_result['wave'] = x
        if self.distance_km >= 3 and self.slope_pct > 3.5:
            if self.progress < 95:
                # todo make calculation more correct should based on 1-self.progress
                x = x / 2
            kp_cat_result['climb'] = x
        return kp_cat_result

@dataclass
class Prediction:
    """The engine's result."""

    # Ordered best -> worst. Use (name, score) if you want to expose scores.
    ranking = []
    summary: str = ""
