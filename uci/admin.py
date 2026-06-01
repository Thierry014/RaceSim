from django.contrib import admin
from .models import Race, Rider, Course, Result, Blog


@admin.register(Race)
class RaceAdmin(admin.ModelAdmin):
    list_display = ['name', 'date', 'category', 'winner', 'predict_winner']
    list_filter = ['category', 'date']
    search_fields = ['name', 'location']


@admin.register(Rider)
class RiderAdmin(admin.ModelAdmin):
    list_display = ['name', 'nationality', 'get_age', 'form', 'form_trend']
    list_filter = ['nationality', 'breakaway']
    search_fields = ['name']

    @admin.display(description='Age', ordering='-date_of_birth')
    def get_age(self, obj):
        return obj.age


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['name', 'winner', 'predict_winner', 'elevation_gain_m', 'get_is_won_by_breakaway', 'get_bingo', 'bingo_rate']
    list_filter = ['race']
    search_fields = ['name']

    @admin.display(description='Breakaway', boolean=True)
    def get_is_won_by_breakaway(self, obj):
        return obj.is_won_by_breakaway

    @admin.display(description='Bingo', boolean=True)
    def get_bingo(self, obj):
        return obj.bingo

@admin.register(Result)
class ResultAdmin(admin.ModelAdmin):
    list_display = ['course', 'rider', 'rank']


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ['title', 'publish_date', 'published']
    list_filter = ['published']
    search_fields = ['title']