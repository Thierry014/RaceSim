"""The prediction logic. Pure Python: takes domain objects, returns a Prediction."""

from .domain import RiderStats, KeyPoint, Prediction

Form = {
    0: 0.8,
    1: 0.85,
    2: 0.9,
    3: 0.95,
    4: 1,
    5: 1.05,
}

class PredictEngine:
    """Scores riders against a course's key points and ranks them.

    Stateless by default; if you later need tunable weights, move them into
    ``__init__`` and read ``self.<weight>`` inside ``predict``.
    """

    @staticmethod
    def predict(riders: list[RiderStats], key_points: list[KeyPoint]) -> Prediction:
        if not riders:
            return Prediction(summary="No riders provided.")

        dropped_from_kp = []
        survive_from_kp = []
        # first rider loop to check they can survive
        for rider in riders:  # sortby score low to high
            for key_point in key_points:
                point_index = key_point.distance_km * (key_point.slope_pct ** 2)
                if rider.limit < point_index:  # should add keypoint 3
                    rider.dropped = True
                    dropped_from_kp.append((rider.name, key_point.position_km))
                    break
            # todo course summary should not just check the kps, it should check course profile as well
            # course_summary = key_points[-1]
            course_summary = [('climb', 70), ('punch', 30)]
            # [('climb', 90), ('punch', 10)]
            if not rider.dropped:
                rdr_score = 0
                for cat in course_summary:
                    cat_name, cat_pct = cat[0], cat[1]/100
                    rdr_ability_score = getattr(rider, f"score_{cat_name}")
                    rdr_score += rdr_ability_score * cat_pct * Form[rider.form]
                survive_from_kp.append((rider.name, "survive", rdr_score))

        # 2nd rider loop to ability/form short list (todo check punch score)
        print("dropped")
        print(dropped_from_kp)
        print("survive")
        result = survive_from_kp.sort(key=lambda row: row[2], reverse=True)
        print(survive_from_kp)
        return result
