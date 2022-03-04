import nested_admin
from django.contrib import admin
from .models import Category, Blog, Comment, Reply, Content, Paragraph, quote, style

class ParagraphInline(nested_admin.NestedTabularInline):
    model = Paragraph
    extra = 0


class ContentInline(nested_admin.NestedTabularInline):
    model = Content
    inlines = [ParagraphInline]

class BlogAdmin(nested_admin.NestedModelAdmin):
    inlines = [ContentInline]
    ordering = ('date',)

class styleadmin(admin.ModelAdmin):
    model = style
    list_display = ['id', 'style']

# Register your models here.
admin.site.register(Category)
admin.site.register(Blog, BlogAdmin)
admin.site.register(Reply)
admin.site.register(quote)
admin.site.register(style, styleadmin)
