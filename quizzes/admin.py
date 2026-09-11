from django.contrib import admin
from .models import Quiz, Question, Result

class QuestionInline(admin.StackedInline):
    model = Question
    extra = 1

@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'lesson', 'passing_score')
    list_filter = ('course',)
    inlines = [QuestionInline]

@admin.register(Result)
class ResultAdmin(admin.ModelAdmin):
    list_display = ('user', 'quiz', 'score', 'passed', 'timestamp')
    list_filter = ('passed', 'quiz')
