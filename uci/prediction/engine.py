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
            last_pt = key_points[-1]
            ability_score = last_pt[-1] # todo should have a function to calculate
            if not rider.dropped:
                # check category of current point, then calculate the socre based on form and speciality
                ability_score = getattr(rider, f"score_{ability_score}")
                score_real = Form[rider.form] * ability_score
                # score_predicted = Form[rider.predict_form] * ability_score
                survive_from_kp.append((rider.name, "survive", score_real))
                # survive_from_kp.append((rider.name, "survive", score_real, score_predicted))

        # 2nd rider loop to ability/form short list (todo check punch score)
        print("dropped")
        print(dropped_from_kp)
        print("survive")
        result = survive_from_kp.sort(key=lambda row: row[2], reverse=True)
        print(survive_from_kp)
        return result
