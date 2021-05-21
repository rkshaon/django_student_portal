from django.db import models
from django.contrib.auth.models import User

class Module(models.Model):
    """docstring for Module."""
    title = models.CharField(max_length=150)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='Module_Owner')
    hours = models.PositiveIntegerField()

    def __str__(self):
        return self.title
