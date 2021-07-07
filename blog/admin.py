from django.contrib import admin
from .models import Post, Category, Tag

# Register your models here.
admin.site.register(Post)


class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)} # Category 모델의 name 필드에 값이 입력되면 자동으로 slug 생성


class TagAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('name',)}


admin.site.register(Category, CategoryAdmin)
admin.site.register(Tag, TagAdmin)

