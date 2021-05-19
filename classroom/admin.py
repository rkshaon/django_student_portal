from django.contrib import admin
from classroom.models import Category, Course

class CategoryAdmin(admin.ModelAdmin):
    """docstring for CategoryAdmin."""
    prepopulated_fields = {"slug": ("title",)}

admin.site.register(Category, CategoryAdmin)
admin.site.register(Course)
