from django.db import models
from ckeditor.fields import RichTextField

from django.contrib.auth.models import User

class Answer(models.Model):
    """docstring for Answer."""
    answer_text = models.CharField(max_length=900)
    is_correct = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def _str__(self):
        return self.answer_text

class Question(models.Model):
    """docstring for Question."""
    question_text = models.CharField(max_length=900)
    answers = models.ManyToManyField(Answer)
    points = models.PositiveIntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.question_text

class Quizzes(models.Model):
    """docstring for Quizzes."""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    content = RichTextField()
    date = models.DateTimeField(auto_now_add=True)
    due = models.DateField()
    allowed_attempts = models.PositiveIntegerField()
    time_limit_mins = models.PositiveIntegerField()
    questions = models.ManyToManyField(Question)

    def __str__(self):
        return self.title

class Attempter(models.Model):
    """docstring for Attempter."""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quizzes, on_delete=models.CASCADE)
    score = models.PositiveIntegerField()
    completed = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username

class Attempt(models.Model):
    """docstring for Attempt."""
    quiz = models.ForeignKey(Quizzes, on_delete=models.CASCADE)
    attempter = models.ForeignKey(Attempter, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE)

    def __str__(self):
        return self.attempter.user.username + ' - ' + self.answer.answer_text
