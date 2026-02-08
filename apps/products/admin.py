from django.contrib import admin
from .models import Category, Product

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    readonly_fields = ['slug']

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'price', 'stock', 'is_active', 'created_at']
    list_filter = ['is_active', 'category', 'created_at']
    list_editable = ['price', 'stock', 'is_active'] # Edit inventory directly from the list view!
    readonly_fields = ['slug', 'created_at', 'updated_at']
    
    # Organizes the fields in the edit form
    fieldsets = (
        ('General Information', {
            'fields': ('name', 'slug', 'category', 'seller', 'description')
        }),
        ('Inventory & Pricing', {
            'fields': ('price', 'stock', 'is_active')
        }),
        ('Media', {
            'fields': ('image',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',) # Hides this section by default
        }),
    )