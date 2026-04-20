from django.contrib import admin
from .models import Race, Rider, Course


@admin.register(Race)
class RaceAdmin(admin.ModelAdmin):
    list_display = ['name', 'date', 'location', 'category']
    list_filter = ['category', 'date']
    search_fields = ['name', 'location']


@admin.register(Rider)
class RiderAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'nationality', 'date_of_birth']
    list_filter = ['nationality']
    search_fields = ['first_name', 'last_name']


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['name', 'race', 'distance_km', 'elevation_gain_m']
    list_filter = ['race']
    search_fields = ['name']
