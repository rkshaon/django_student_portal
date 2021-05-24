from django.db import models
from django.contrib.auth.models import User

from page.models import Page

class Module(models.Model):
    """docstring for Module."""
    title = models.CharField(max_length=150)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='Module_Owner')
    hours = models.PositiveIntegerField()
    pages = models.ManyToManyField(Page, related_name='Module_Page')

    def __str__(self):
        return self.title
