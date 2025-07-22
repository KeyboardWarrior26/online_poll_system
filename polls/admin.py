from django.contrib import admin
from .models import Question, Choice

class ChoiceInline(admin.TabularInline):  # or use StackedInline
    model = Choice
    extra = 3  # how many extra blank choices to show

class QuestionAdmin(admin.ModelAdmin):
    list_display = ('question_text', 'pub_date', 'was_published_recently')
    list_filter = ['pub_date']
    search_fields = ['question_text']
    inlines = [ChoiceInline]

admin.site.register(Question, QuestionAdmin)

