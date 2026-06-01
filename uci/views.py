from django.shortcuts import render, get_object_or_404
from .models import Race, Rider, Course


def index(request):
    races = Race.objects.all()
    riders = Rider.objects.all()
    courses = Course.objects.all()

    context = {
        'total_races': races.count(),
        'total_riders': riders.count(),
        'total_courses': courses.count(),
        'recent_races': races.order_by('-date')[:10],
    }
    return render(request, 'uci/index.html', context)

def course_list(request):
    courses = Course.objects.all().order_by('-pk')
    return render(request, 'uci/course_list.html', {'courses': courses})

def course_detail(request, pk):
    course = get_object_or_404(Course, pk=pk)
    return render(request, 'uci/course_detail.html', {'course': course})
