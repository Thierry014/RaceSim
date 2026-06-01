from django.urls import path
from . import views

app_name = 'uci'

urlpatterns = [
    path('', views.index, name='index'),
    path('course/', views.course_list, name='course_list'),
    path('course/<int:pk>/', views.course_detail, name='course_detail'),
    # path('race/', views.race_list, name='race_list'),
    # path('rider/', views.rider_list, name='rider_list'),
]
