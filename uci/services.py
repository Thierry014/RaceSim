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
        predict_form=rider.predict_form,
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
        key_points = [KeyPoint(*kp, progress=round(float(kp[-1]/course.distance_km * 100),2)) for kp in course.key_point]
    if course.course_summary:
        course_summary = course.course_summary
    return key_points, course_summary

def _kps_to_summary(key_points, climb_per_km):
    course_summary = {}
    score = 100
    # flat stage
    if not key_points:
        return {'sprint': score}
    reverse_kps = key_points[::-1]
    # print(reverse_kps)
    for kp in reverse_kps:
        # determine category, determine pct based on progress
        # print(kp.kp_cat)
        for x in kp.kp_cat.keys():
            if kp.progress > 70:
                if x in course_summary:
                    course_summary[x] += kp.kp_cat[x]
                else:
                    course_summary[x] = kp.kp_cat[x]
    total = sum(course_summary.values())
    if len(reverse_kps):
        # sprint calibration
        last_kp = reverse_kps[-1]
        if last_kp.progress < 95:
            if not course_summary.get("sprint"):
                course_summary["sprint"] = total * 0.2
    # climb calibration
    # todo may be a non0linier number to calibrate like Y=X*K ?
    if climb_per_km:
        if climb_per_km > 15:
            course_summary["climb"] += total * 0.15
        elif climb_per_km > 25:
            course_summary["climb"] += total * 0.3
    return course_summary

def predict_course(course: Course, riders_qs, use_auto, current_form) -> str:
    """Run the engine for a course over the given riders queryset."""
    riders = [_to_stats(r) for r in riders_qs]
    key_points, course_summary = _prepare_course(course)
    auto_course_summary = _kps_to_summary(key_points, course.climb_per_km)
    if not course.course_summary or use_auto:
        summary = auto_course_summary
    # use user input
    else:
        summary = course_summary
    climb_per_km = course.climb_per_km
    prediction_result =  PredictEngine.predict(riders, key_points, summary, climb_per_km, current_form)
    txt_result = f"auto: {use_auto}, current_form: {current_form} \n"
    for k, v in prediction_result.items():
        txt_result += f"{k}: {v} \n"
    return txt_result
