from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden
from django.template import loader

from module.forms import NewModuleForm

from module.models import Module
from classroom.models import Course

def new_module(request, course_id):
    user = request.user
    course = get_object_or_404(Course, id=course_id)

    if user != course.user:
        return HttpResponseForbidden()
    else:
        if request.method == 'POST':
            form = NewModuleForm(request.POST)
            if form.is_valid():
                title = form.cleaned_data.get('title')
                hours = form.cleaned_data.get('hours')

                m, created = Module.objects.get_or_create(title=title, hours=hours, user=user)
                course.modules.add(m)
                course.save()

                # return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
                return redirect('course_modules', course_id=course_id)
        else:
            form = NewModuleForm()

    context = {
        'form': form,
    }

    template = loader.get_template('module/newmodule.html')
    return HttpResponse(template.render(context, request))

def course_modules(request, course_id):
    user = request.user
    course = get_object_or_404(Course, id=course_id)
    teacher_mode = False

    if user == course.user:
        teacher_mode = True

    context = {
        'teacher_mode': teacher_mode,
        'course': course,
    }

    template = loader.get_template('module/modules.html')
    return HttpResponse(template.render(context, request))
