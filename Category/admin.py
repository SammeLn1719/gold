from django.contrib import admin
from .models import Category, Product

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'description']
    search_fields = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}
    list_filter = ['name']

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'price', 'stock', 'image']
    search_fields = ['name', 'description']
    list_filter = ['category']
    readonly_fields = ['get_image_preview']

    def get_image_preview(self, obj):
        if obj.image:
            return f'<img src="{obj.get_image_url()}" style="max-height: 100px; max-width: 100px;" />'
        return "Нет изображения"
    get_image_preview.short_description = 'Превью'
    get_image_preview.allow_tags = True