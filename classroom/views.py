from django.shortcuts import render, redirect, get_object_or_404
from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden
from django.contrib.auth.decorators import login_required

from classroom.models import Category, Course

from classroom.forms import NewCourseForm

def index(request):
    user = request.user
    courses = Course.objects.filter(enrolled=user)

    context = {
        'courses': courses,
    }

    template = loader.get_template('index.html')
    return HttpResponse(template.render(context, request))

def categories(request):
    categories = Category.objects.all()

    context = {
        'categories': categories,
    }

    template = loader.get_template('classroom/categories.html')
    return HttpResponse(template.render(context, request))

def category_courses(request, category_slug):
    category = get_object_or_404(Category, slug=category_slug)
    courses = Course.objects.filter(category=category)

    context = {
        'category': category,
        'courses': courses
    }

    template = loader.get_template('classroom/categorycourses.html')
    return HttpResponse(template.render(context, request))

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

            Course.objects.create(picture=picture, title=title, description=description, category=category, syllabus=syllabus, user=user)
            return redirect('my_courses')
    else:
        form = NewCourseForm()

    context = {
        'form': form,
    }

    template = loader.get_template('classroom/newcourse.html')
    return HttpResponse(template.render(context, request))

def course_details(request, course_id):
    user = request.user
    course = get_object_or_404(Course, id=course_id)
    teacher_mode = False

    if user == course.user:
        teacher_mode = True

    context = {
        'teacher_mode': teacher_mode,
        'course': course,
    }

    template = loader.get_template('classroom/course.html')
    return HttpResponse(template.render(context, request))

@login_required
def enroll(request, course_id):
    user = request.user
    course = get_object_or_404(Course, id=course_id)
    course.enrolled.add(user)

    return redirect('index')

@login_required
def delete_course(request, course_id):
    user = request.user
    course = get_object_or_404(Course, id=course_id)

    if user != course.user:
        return HttpResponseForbidden()
    else:
        course.delete()

    return redirect('my_courses')

@login_required
def edit_course(request, course_id):
    user = request.user
    course = get_object_or_404(Course, id=course_id)

    if user != course.user:
        return HttpResponseForbidden()
    else:
        if request.method == 'POST':
            form = NewCourseForm(request.POST, request.FILES, instance=course)
            if form.is_valid():
                course.picture = form.cleaned_data.get('picture')
                course.title = form.cleaned_data.get('title')
                course.description = form.cleaned_data.get('description')
                course.category = form.cleaned_data.get('category')
                course.syllabus = form.cleaned_data.get('syllabus')
                course.save()

                return redirect('my_courses')
        else:
            form = NewCourseForm(instance=course)

    context = {
        'form': form,
        'course': course,
    }

    template = loader.get_template('classroom/editcourse.html')
    return HttpResponse(template.render(context, request))

def my_courses(request):
    user = request.user
    courses = Course.objects.filter(user=user)

    context = {
        'courses': courses,
    }

    template = loader.get_template('classroom/mycourses.html')
    return HttpResponse(template.render(context, request))
