"""Adapter layer: the only place that bridges the Django ORM and the pure
prediction engine. Views call these functions; they never touch the engine
directly.
"""

from .models import Course, Rider
from .prediction import RiderStats, KeyPoint, PredictEngine, Prediction


def _to_stats(rider: Rider) -> RiderStats:
    """Map a Django ``Rider`` to the engine's plain ``RiderStats``."""
    return RiderStats(
        name=rider.name,
        form=rider.form,
        breakaway=rider.breakaway,
        score_climb=rider.score_climb,
        score_wave=rider.score_wave,
        score_punch=rider.score_punch,
        score_tt=rider.score_tt,
        score_sprint=rider.score_sprint,
        score_steep=rider.score_steep,
        limit_distance=rider.limit_distance,
        limit_slope=rider.limit_slope,
    )


def _to_key_points(course: Course) -> list[KeyPoint]:
    """Turn ``course.key_point`` (a list of triples) into KeyPoint objects.

    Legacy rows may hold a free-text string instead of a list; those are skipped.
    """
    raw = course.key_point
    if not isinstance(raw, list):
        return []
    return [KeyPoint(*kp, progress=kp[-1]/course.distance_km * 100) for kp in raw]


def predict_course(course: Course, riders_qs) -> Prediction:
    """Run the engine for a course over the given riders queryset."""
    riders = [_to_stats(r) for r in riders_qs]
    key_points = _to_key_points(course)
    return PredictEngine.predict(riders, key_points)