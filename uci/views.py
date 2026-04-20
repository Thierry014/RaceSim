from django.shortcuts import render
from .models import Race, Rider, Course


def index(request):
    races = Race.objects.all()
    riders = Rider.objects.all()
    courses = Course.objects.all()

    context = {
        'total_races': races.count(),
        'total_riders': riders.count(),
        'total_courses': courses.count(),
        'recent_races': races.order_by('-date')[:5],
    }

    return render(request, 'uci/index.html', context)
