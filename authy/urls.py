from django.urls import path

from django.contrib.auth import views as authViews
from authy.views import PasswordChange, PasswordChangeDone
from authy.views import sign_up, edit_profile, user_profile

urlpatterns = [
    path('profile/edit', edit_profile, name='edit_profile'),
   	path('signup/', sign_up, name='signup'),
   	path('login/', authViews.LoginView.as_view(template_name='registration/login.html'), name='login'),
   	path('logout/', authViews.LogoutView.as_view(), {'next_page' : 'index'}, name='logout'),
   	path('changepassword/', PasswordChange, name='change_password'),
   	path('changepassword/done', PasswordChangeDone, name='change_password_done'),
   	path('passwordreset/', authViews.PasswordResetView.as_view(), name='password_reset'),
   	path('passwordreset/done', authViews.PasswordResetDoneView.as_view(), name='password_reset_done'),
   	path('passwordreset/<uidb64>/<token>/', authViews.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
   	path('passwordreset/complete/', authViews.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]
