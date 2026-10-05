from django.contrib import admin
from .models import Category, Item

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'icon')
    search_fields = ('name',)

@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'item_type', 'category', 'location', 'date_occurred', 'status', 'reported_by')
    list_filter = ('item_type', 'category', 'location', 'status')
    search_fields = ('title', 'description', 'specific_location_details')
    date_hierarchy = 'created_at'
