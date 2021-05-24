from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_requird
from django.http import HttpResponseForbidden

from page.models import Page, PostFileContent
from classroom.models import Course
from module.models import Module

from page.forms import NewPageForm

@login_requird
def new_page_module(request, course_id, module_id):
    user = request.user
    course = get_object_or_404(Course, id=course_id)
    module = get_object_or_404(Module, id=module_id)
    files_objs = []

    if user != course.user:
        return HttpResponseForbidden
    else:
        if request.method == 'POST':
            form = NewPageForm(request.POST, request.FILES)
            if form.is_valid():
                title = forms.cleaned_data.get('title')
                content = forms.cleaned_data.get('content')
                files = request.FILES.getlist('files')

                for file in files:
                    file_instance = PostFileContent(file=file, user=user)
                    file_instance.save()
                    files_objs.append(file_instance)

                p = Page.objects.create(title=title, content=content, user=user)
                p.files.set(files_objs)
                p.save()
                module.pages.add(p)
                return redirect('my_courses')
        else:
            form = NewPageForm()

    context = {
        'form': form,
    }

    template = loader.get_template('page/newpage.html')
    return HttpResponse(template.render(context, request))

def page_details(request, course_id, page_id):
    page = get_object_or_404(Page, id=page_id)

    context = {
        'page': page,
    }

    template = loader.get_template('page/page.html')
    return HttpResponse(template.render(context, request))
