from django.urls import path

from classroom.views import categories, category_courses, new_course, enroll, delete_course, edit_course, my_courses

urlpatterns = [
    # course - clasroom views
    path('new-course/', new_course, name='new_course'),
    path('my-courses/', my_courses, name='my_courses'),
    path('categories/', categories, name='categories'),
    path('category/<category_slug>', category_courses, name='category_courses'),
    path('<course_id>/enroll/', enroll, name='enroll'),
    path('<course_id>/edit', edit_course, name='edit_course'),
    path('<course_id>/delete', delete_course, name='delete_course'),
]
