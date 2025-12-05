from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import Homework, Doubt, StudentProfile, Assignment

# Define an inline admin descriptor for StudentProfile model
class StudentProfileInline(admin.StackedInline):
    model = StudentProfile
    can_delete = False
    verbose_name_plural = 'student_profile'

# Define a new User admin
class UserAdmin(BaseUserAdmin):
    inlines = (StudentProfileInline,)

# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)

admin.site.register(Homework)
admin.site.register(Doubt)
admin.site.register(Assignment)
