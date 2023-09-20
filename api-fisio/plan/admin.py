from django.contrib import admin
from .models import Plan, Exercise, ExerciseVideo


class ExerciseInline(admin.TabularInline):
    model = Plan.exercise_set.through
    extra = 1

@admin.register(Plan)
class PlanAdmin(admin.ModelAdmin):
    inlines = (ExerciseInline,)
    list_display = ('id', 'title', 'get_custom_short_description', 'created_at', 'updated_at')

    def get_custom_short_description(self, obj):
        description = obj.description
        if len(description) >= 30:
            return obj.description[0:30] + '...'
        else:
            return obj.description

    get_custom_short_description.short_description = 'Description'

    def __str__(self):
            return self.title


@admin.register(Exercise)
class ExerciseAdmin(admin.ModelAdmin):
    list_display = ('id', 'name',)


@admin.register(ExerciseVideo)
class ExerciseVideoAdmin(admin.ModelAdmin):
    list_display = ('id', 'name',)


