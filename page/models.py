from django.db import models
import os
from ckeditor.fields import RichTextField

from django.contrib.auth.models import User

from classroom.models import user_directory_path

class PostFileContent(models.Model):
    """docstring for PostFileContent."""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    file = models.FileField(upload_to=user_directory_path)
    posted = models.DateTimeField(auto_now_add=True)

    def get_file_name(self):
        return os.path.basename(self.file.name)

class Page(models.Model):
    """docstring for Page."""
    title = models.CharField(max_length=150)
    content = RichTextField()
    files = models.ManyToManyField(PostFileContent)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='Page_Owner')

    def __str__(self):
        return self.title
