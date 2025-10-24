from django.contrib import admin
from .models import Question, Choice


# Create an Inline for Choices
class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 3  # Shows 3 blank choices by default

# Customize Question admin to include choices
class QuestionAdmin(admin.ModelAdmin):
    inlines = [ChoiceInline]

# Register models
admin.site.register(Question, QuestionAdmin)
admin.site.register(Choice)