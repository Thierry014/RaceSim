from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Race, Rider, Course, Bet


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
    bets = Bet.objects.filter(course=course).select_related('user', 'rider')
    riders = Rider.objects.all()
    users = User.objects.all()
    return render(request, 'uci/course_detail.html', {'course': course, 'bets': bets, 'riders': riders, 'users': users})


# @login_required
def bet_create(request, course_pk):
    course = get_object_or_404(Course, pk=course_pk)
    if request.method == 'POST':
        user_id = request.POST.get('user')
        rider_id = request.POST.get('rider')
        odd_rate = request.POST.get('odd_rate')
        bet_amount = request.POST.get('bet_amount')
        user = get_object_or_404(User, pk=user_id)
        rider = get_object_or_404(Rider, pk=rider_id)
        Bet.objects.create(
            user=user,
            course=course,
            rider=rider,
            odd_rate=odd_rate,
            bet_amount=bet_amount,
        )
    return redirect('uci:course_detail', pk=course_pk)
