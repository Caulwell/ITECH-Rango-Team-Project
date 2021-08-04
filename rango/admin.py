from django.contrib import admin
from rango.models import Category, Page, Subcategory, UserProfile

# Register your models here.

class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug":("name",)}

class SubcategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug":("name",)}

class PageAdmin(admin.ModelAdmin):
    list_display = ("name", "subcategory", "url")

admin.site.register(Category, CategoryAdmin)
admin.site.register(Subcategory, SubcategoryAdmin)
admin.site.register(Page, PageAdmin)
admin.site.register(UserProfile)