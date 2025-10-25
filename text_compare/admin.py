from django.contrib import admin

# Register your models here.
# text_compare/admin.py
from .models import TextComparison

@admin.register(TextComparison)
class TextComparisonAdmin(admin.ModelAdmin):
    list_display = ('id', 'created_at', 'left_text', 'right_text')
    readonly_fields = ('created_at',)
    list_filter = ["created_at"]
    search_fields = ["left_text", "right_text"]
