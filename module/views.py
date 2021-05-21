from django.shortcuts import render, redirect, get_object_or_404

from module.forms import NewModuleForm

from module.models import Module
from classroom.models import Course

def new_module(request, course_id):
    user = request.user
    course = get_object_or_404(Course, id=course_id)

    if request.method == 'POST':
        form = NewModuleForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data.get('title')
            hours = form.cleaned_data.get('hours')

            m, created = Module.objects.get_or_create(title=title, hours=hours, user=user)
            
