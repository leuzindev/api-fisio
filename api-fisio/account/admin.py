from django.contrib import admin
from account.models import User

class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'is_superuser')




admin.site.register(User, UserAdmin)