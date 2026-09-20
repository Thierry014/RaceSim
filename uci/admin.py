from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import Race, Rider, Course, Result, Blog, UserProfile, Bet


class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False


class CustomUserAdmin(UserAdmin):
    inlines = [UserProfileInline]
    list_display = UserAdmin.list_display + ('get_credit',)

    @admin.display(description='Credit')
    def get_credit(self, obj):
        try:
            return obj.profile.credit
        except UserProfile.DoesNotExist:
            return '-'


admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)


@admin.register(Race)
class RaceAdmin(admin.ModelAdmin):
    list_display = ['name', 'date', 'category', 'winner', 'predict_winner']
    list_filter = ['category', 'date']
    search_fields = ['name', 'location']


@admin.register(Rider)
class RiderAdmin(admin.ModelAdmin):
    list_display = ['name', 'form', 'form_trend', 'attack_index', 'score_climb', 'score_tt', 'score_wave', 'score_punch', 'score_sprint']
    list_filter = ['nationality', 'breakaway', 'watch_listed']
    search_fields = ['name']

    @admin.display(description='Age', ordering='-date_of_birth')
    def get_age(self, obj):
        return obj.age


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['name', 'winner', 'predict_winner', 'profile_score', 'get_is_won_by_breakaway', 'get_bingo', 'bingo_rate']
    list_filter = ['race']
    search_fields = ['name']

    @admin.display(description='Breakaway', boolean=True)
    def get_is_won_by_breakaway(self, obj):
        return obj.is_won_by_breakaway

    @admin.display(description='Bingo', boolean=True)
    def get_bingo(self, obj):
        return obj.bingo

# @admin.register(Result)
# class ResultAdmin(admin.ModelAdmin):
#     list_display = ['course', 'rider', 'rank']


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ['title', 'publish_date', 'published']
    list_filter = ['published']
    search_fields = ['title']


@admin.register(Bet)
class BetAdmin(admin.ModelAdmin):
    list_display = ['user', 'rider', 'course', 'bet_amount', 'odd_rate', 'credit_return', 'status']
    list_filter = ['status']
    search_fields = ['user__username', 'rider__name']
