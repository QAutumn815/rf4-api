from django.contrib import admin

from apps.core.models import AbsoluteRecord, WeeklyRecord, Rating, Winner


@admin.register(AbsoluteRecord)
class AbsoluteRecordAdmin(admin.ModelAdmin):
    list_display = ("fish", "fish_image", "weight", "player", "region", "category", "date")
    list_filter = ("region", "category", "fish")
    search_fields = ("player", "fish", "location")
    date_hierarchy = "date"


@admin.register(WeeklyRecord)
class WeeklyRecordAdmin(admin.ModelAdmin):
    list_display = ("fish", "fish_image", "weight", "player", "region", "category", "date")
    list_filter = ("region", "category", "fish")
    search_fields = ("player", "fish", "location")
    date_hierarchy = "date"


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ("position", "player", "level", "ingame", "region")
    list_filter = ("region",)
    search_fields = ("player",)


@admin.register(Winner)
class WinnerAdmin(admin.ModelAdmin):
    list_display = ("position", "player", "score", "region", "category")
    list_filter = ("region", "category")
    search_fields = ("player",)
