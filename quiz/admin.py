from django.contrib import admin

from quiz.models import Answer, Question, Quizzes, Attempter, Attempt

admin.site.register(Answer)
admin.site.register(Question)
admin.site.register(Quizzes)
admin.site.register(Attempter)
admin.site.register(Attempt)
