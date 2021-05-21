from django.db import models
from django.urls import reverse
from django.utils.text import slugify
import uuid
# Third party fields
from ckeditor.fields import RichTextField

from django.contrib.auth.models import User

def user_directory_path(instance, filename):
    # This file will be uploaded to MEDIA/{user_id}/filename
    return 'user_{0}/{1}'.format(instance.user.id, filename)

class Category(models.Model):
    """docstring for Category."""
    title = models.CharField(max_length=100, verbose_name='Title')
    icon = models.CharField(max_length=100, verbose_name='Icon', default='article')
    slug = models.SlugField(unique=True)

    def get_absolute_url(self):
        return reverse('categories', arg=[self.slug])

    def __str__(self):
        return self.title

class Course(models.Model):
    """docstring for Course."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    picture = models.ImageField(upload_to=user_directory_path)
    title = models.CharField(max_length=200)
    description = models.CharField(max_length=300)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    syllabus = RichTextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='Course_Owner')
    enrolled = models.ManyToManyField(User, related_name='Enrolled_User')

    def __str__(self):
        return self.title
