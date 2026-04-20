from django.urls import path
from . import views

app_name = 'uci'

urlpatterns = [
    path('', views.index, name='index'),
    # path('race/', views.race_list, name='race_list'),
    # path('rider/', views.rider_list, name='rider_list'),
]
