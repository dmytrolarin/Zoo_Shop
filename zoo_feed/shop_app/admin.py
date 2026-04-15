from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import*


class AdminMixin:
    """Mixin with shared methods for admin classes."""

    # Display the image preview in the admin panel.
    def image_show(self, obj):
        if obj.image:
            return mark_safe(f"<img src='{obj.image.url}' width = '60' />")
        return None

    image_show.__name__ = 'Image'


class TypeOfProductAdmin(admin.ModelAdmin, AdminMixin):
    list_display = ('name','image_show')


class FilterGroupAdmin(admin.ModelAdmin):
    list_display = ('title',)
    search_fields = ('title',)
    prepopulated_fields = {'slug': ('title',)}


class FilterItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'filter_group')
    search_fields = ('name', 'filter_group')
    prepopulated_fields = {'slug': ('name',)}


class BrandAdmin(admin.ModelAdmin, AdminMixin):
    list_display = ('name', 'image_show', )
    search_fields = ('name',)

class PackingInlineAdmin(admin.TabularInline):
    model = Packing  
    extra = 0

class ProductAdmin(admin.ModelAdmin, AdminMixin):
    list_display = ('name', 'vendor_code', 'image_show')
    search_fields = ('name', 'vendor_code')
    inlines =  [PackingInlineAdmin,]

    
class PackingAdmin(admin.ModelAdmin):
    list_display = ('product', 'weight', 'current_price')


admin.site.register(TypeOfProduct, TypeOfProductAdmin)
admin.site.register(FilterGroup, FilterGroupAdmin)
admin.site.register(FilterItem, FilterItemAdmin)
admin.site.register(Brand, BrandAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Packing, PackingAdmin)
