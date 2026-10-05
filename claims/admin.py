from django.contrib import admin
from .models import ClaimRequest

@admin.register(ClaimRequest)
class ClaimRequestAdmin(admin.ModelAdmin):
    list_display = ('item', 'claimant', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('item__title', 'claimant__username', 'answer_to_secret_mark')
