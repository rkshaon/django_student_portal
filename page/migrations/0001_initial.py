# Generated by Django 3.1.7 on 2021-05-22 21:39

import ckeditor.fields
import classroom.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='PostFileContent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to=classroom.models.user_directory_path)),
                ('posted', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Page',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=150)),
                ('content', ckeditor.fields.RichTextField()),
                ('files', models.ManyToManyField(to='page.PostFileContent')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Page_Owner', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
