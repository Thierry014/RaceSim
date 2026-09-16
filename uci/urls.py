from django.urls import path
from . import views

app_name = 'uci'

urlpatterns = [
    path('', views.index, name='index'),
    path('course/', views.course_list, name='course_list'),
    path('course/<int:pk>/', views.course_detail, name='course_detail'),
    path('course_predict/<int:pk>', views.course_predict, name='course_predict'),
    path('course/<int:course_pk>/bet/', views.bet_create, name='bet_create'),
    path('course/<int:course_pk>/settle/', views.bet_settle, name='bet_settle'),
    # path('race/', views.race_list, name='race_list'),
    # path('rider/', views.rider_list, name='rider_list'),
]
