from django.shortcuts import render, redirect
from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect

from classroom.models import Category, Course

from classroom.form import NewCourseForm

def index(request):
    user = request.user
    

def new_course(request):
    user = request.user

    if request.method == 'POST':
        form = NewCourseForm(request.POST, request.FILES)
        if form.is_valid():
            picture = form.cleaned_data.get('picture')
            title = form.cleaned_data.get('title')
            description = form.cleaned_data.get('description')
            category = form.cleaned_data.get('category')
            syllabus = form.cleaned_data.get('syllabus')

            Course.objects.create(picture=picture, title=title, description=description, category=category, syllabus=syllabus)
            return redirect('my_courses')
    else:
        form = NewCourseForm()

    context = {
        'form': form,
    }

    template = loader.get_template('classroom/newcourse.html')

    return HttpResponse(template.render(context, request))
