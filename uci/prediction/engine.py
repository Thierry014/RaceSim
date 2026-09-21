"""The prediction logic. Pure Python: takes domain objects, returns a Prediction."""
from locale import normalize

from .domain import RiderStats, KeyPoint, Prediction

Form = {
    0: 0.8,
    1: 0.85,
    2: 0.9,
    3: 0.95,
    4: 1,
    5: 1.05,
}

# CLIMB_PER_METER = {
#     "normal": {
#         "flat": "0~5",
#         "wave": "5~20",
#         "climb": ">20",
#     },
#     "tt": {
#         "flat": "0~15",
#         "climb": ">10",
#     }
#
# }

# course_summary = {"a": xxx, "b":xxx}
class PredictEngine:
    """Scores riders against a course's key points and ranks them.

    Stateless by default; if you later need tunable weights, move them into
    ``__init__`` and read ``self.<weight>`` inside ``predict``.
    """

    @staticmethod
    def predict(riders: list[RiderStats], key_points: list[KeyPoint], course_summary: dict, current_form:bool =True):
        if not riders:
            return Prediction(summary="No riders provided.")
        dropped_from_kp = []
        survive_from_kp = []
        normalized_course_summary = {}
        all_vals = sum(course_summary.values())
        for key in course_summary.keys():
            normalized_course_summary[key] = round((course_summary[key] / all_vals * 100), 2)
        # print(key_points)
        print(course_summary)
        print(normalized_course_summary)

        # first rider loop to check they can survive and how good they can
        for rider in riders:
            form_to_use = rider.form if current_form else rider.predict_form
            for key_point in key_points:
                point_index = key_point.distance_km * (key_point.slope_pct ** 2)
                if rider.limit < point_index:  # should add keypoint 3
                    rider.dropped = True
                    dropped_from_kp.append((rider.name, key_point.position_km))
                    break
            # todo course summary should not just check the kps, it should check course profile as well
            if not rider.dropped:
                rdr_score = 0
                for cat in normalized_course_summary.keys():
                    cat_name, cat_pct = cat, normalized_course_summary[cat]/100
                    rdr_ability_score = getattr(rider, f"score_{cat_name}")
                    rdr_score += rdr_ability_score * cat_pct * Form[form_to_use]
                    rdr_score = round(rdr_score, 2)
                survive_from_kp.append((rider.name, "survive", rdr_score))

        # normal prediction
        print("dropped")
        print(dropped_from_kp)
        print("survive")
        survive_from_kp.sort(key=lambda row: row[2], reverse=True)
        print(survive_from_kp)

        # 2nd rider loop to ability/form short list (todo check punch score)
        attack_list = []
        rdr_to_attack = [ r for r in riders if r.attack_index > 0]
        for rdr in rdr_to_attack:
            to_add = False
            for x in normalized_course_summary:
                # Todo more rules to determine whether go
                index = 50
                match x:
                    case "climb":
                        ...
                    case _:
                        ...
            if to_add and rdr not in attack_list:
                attack_list.append(rdr.name)
        print("Might attack")
        print(attack_list)
        result = {"dropped": dropped_from_kp, "survive": survive_from_kp, "attack":attack_list, "normalized": normalized_course_summary}
        return result

    @staticmethod
    def predict_tt():
        ...