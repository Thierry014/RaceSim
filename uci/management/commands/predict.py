"""Quick prediction runner — edit the CONFIG below and run:

    python manage.py predict

No UI, no command-line args. Just change the values here.
"""

from django.core.management.base import BaseCommand

from uci.models import Course, Rider
from uci.services import predict_course

# ---------------------------------------------------------------------------
# CONFIG — edit these
# ---------------------------------------------------------------------------
USE_AUTO = True
COURSE_PK = 157            # which course to predict
RIDER_PKS = [224,33,32,14, 51]         # None = all riders, or a list e.g. [3, 5, 7]
# ---------------------------------------------------------------------------


class Command(BaseCommand):
    help = "Run the prediction engine for a hardcoded course without the UI."

    def handle(self, *args, **options):
        course = Course.objects.get(pk=COURSE_PK)

        riders_qs = Rider.objects.all()
        if RIDER_PKS is not None:
            riders_qs = riders_qs.filter(pk__in=RIDER_PKS)

        self.stdout.write(f"Predicting course {course.pk} ({course}) over {riders_qs.count()} riders...")
        prediction = predict_course(course, riders_qs, USE_AUTO)
        self.stdout.write(self.style.SUCCESS("Result:"))
        self.stdout.write(repr(prediction))
