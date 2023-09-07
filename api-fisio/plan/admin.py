from django.contrib import admin
from .models import Plan


@admin.register(Plan)
class PlanAdmin(admin.ModelAdmin):
    list_display = ('title', 'get_custom_short_description', 'created_at', 'updated_at')

    def get_custom_short_description(self, obj):
        description = obj.description
        if len(description) >= 30:
            return obj.description[0:30] + '...'
        else:
            return obj.description

    get_custom_short_description.short_description = 'Description'

    def __str__(self):
            return self.title
