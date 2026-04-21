from django.contrib import admin
from .models import Race, Rider, Course, Result


@admin.register(Race)
class RaceAdmin(admin.ModelAdmin):
    list_display = ['name', 'date', 'category', 'winner', 'predict_winner']
    list_filter = ['category', 'date']
    search_fields = ['name', 'location']


@admin.register(Rider)
class RiderAdmin(admin.ModelAdmin):
    list_display = ['name', 'nationality', 'age', 'form']
    list_filter = ['nationality']
    search_fields = ['name']


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['name', 'winner']
    list_filter = ['race']
    search_fields = ['name']

@admin.register(Result)
class ResultAdmin(admin.ModelAdmin):
    list_display = ['course', 'rider', 'rank']