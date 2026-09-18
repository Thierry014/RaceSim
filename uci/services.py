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
        attack_index=rider.attack_index
    )


def _prepare_course(course: Course):
    """Turn ``course.key_point`` (a list of triples) into KeyPoint objects.

    Legacy rows may hold a free-text string instead of a list; those are skipped.
    """

    key_points = []
    course_summary = {}
    if course.key_point:
        key_points = [KeyPoint(*kp, progress=float(kp[-1]/course.distance_km * 100)) for kp in course.key_point]
    if course.course_summary:
        course_summary = course.course_summary
    return key_points, course_summary

def _kps_to_summary(key_points):
    course_summary = {}
    score = 100
    # flat stage
    if not key_points:
        return {'sprint': score}
    reverse_kps = key_points[::-1]
    print(reverse_kps)
    for kp in reverse_kps:
        # determine category, determine pct based on progress
        print(kp.kp_cat)
        for x in kp.kp_cat.keys():
            if kp.progress > 70:
                if x in course_summary:
                    course_summary[x] += kp.kp_cat[x]
                else:
                    course_summary[x] = kp.kp_cat[x]
    return course_summary

def predict_course(course: Course, riders_qs, use_auto) -> Prediction:
    """Run the engine for a course over the given riders queryset."""
    riders = [_to_stats(r) for r in riders_qs]
    key_points, course_summary = _prepare_course(course)
    new_course_summary = _kps_to_summary(key_points)
    if not course.course_summary or use_auto:
        summary = new_course_summary
    # use user input
    else:
        summary = course_summary
    # to use new for now
    climb_per_km = course.elevation_gain_m / course.distance_km
    prediction_result =  PredictEngine.predict(riders, key_points, summary, climb_per_km)
    # to txt
    txt_result = ""
    for k, v in prediction_result.items():
        txt_result += f"{k}: {v} \n"
    return txt_result
