from django.contrib import admin
from .models import User, Patient, Physiotherapist

class PatientInline(admin.TabularInline):
    model = Patient

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'is_superuser', 'role')
    list_filter = ['role']

    def __str__(self):
        return self.username


@admin.register(Physiotherapist)
class PhysiotherapistAdmin(admin.ModelAdmin):
    list_display = ('username', 'get_patients', 'get_patients_number')
    readonly_fields = ('get_patients',)
    inlines = [PatientInline]

    def username(self, obj):
        return obj.user.username

    def get_patients(self, obj):
        patients = obj.patients.all()
        return ", ".join([patient.user.username for patient in patients])

    get_patients.short_description = 'Patients'

    def get_patients_number(self, obj):
        patients_number = obj.patients.count()
        return patients_number

    get_patients_number.short_description = 'Number of Patients'

    def change_view(self, request, object_id, form_url='', extra_context=None):
        extra_context = extra_context or {}
        physiotherapist = Physiotherapist.objects.get(pk=object_id)
        patients = physiotherapist.patients.all()
        extra_context['patients'] = patients
        return super().change_view(request, object_id, form_url, extra_context=extra_context)

    def __str__(self):
        return self.user.username


@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ('username', 'user', 'physiotherapist',)

    def username(self, obj):
        return obj.user.username

    def __str__(self):
        return self.user.username

