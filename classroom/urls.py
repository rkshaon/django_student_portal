from django.urls import path

from classroom.views import categories, category_courses, new_course, course_details, enroll, delete_course, edit_course, my_courses, enrolled_courses
from module.views import new_module, course_modules
from page.views import new_page_module, page_details

urlpatterns = [
    # course - clasroom views
    path('new-course/', new_course, name='new_course'),
    path('my-courses/', my_courses, name='my_courses'),
    path('enrolled-courses/', enrolled_courses, name='enrolled_courses'),
    path('categories/', categories, name='categories'),
    path('category/<category_slug>/courses', category_courses, name='category_courses'),
    path('<course_id>', course_details, name='course_details'),
    path('<course_id>/enroll/', enroll, name='enroll'),
    path('<course_id>/edit', edit_course, name='edit_course'),
    path('<course_id>/delete', delete_course, name='delete_course'),
    # modules - module views
    path('<course_id>/modules', course_modules, name='course_modules'),
    path('<course_id>/new-module', new_module, name='new_module'),
    # page - page views
    path('<course_id>/modules/<module_id>/new-page', new_page_module, name='new_page_module'),
    path('<course_id>/modules/<module_id>/page/<page_id>', page_details, name='page_details'),
]
