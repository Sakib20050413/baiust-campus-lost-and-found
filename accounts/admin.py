from django.contrib import admin
from .models import UserProfile

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'student_id', 'department', 'phone_number')
    search_fields = ('user__username', 'user__first_name', 'user__last_name', 'student_id', 'phone_number')
    list_filter = ('department',)
