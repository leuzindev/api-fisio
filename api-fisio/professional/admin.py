from django.contrib import admin
from professional.models import Professional


class ProfessionalAdmin(admin.ModelAdmin):
    pass


admin.site.register(Professional, ProfessionalAdmin)