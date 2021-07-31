from django.contrib import admin
from django.urls import path, include
from . import views
from .views import UserEditView,PasswordsChangeView,EditProfilePageView

app_name = "user"

urlpatterns = [
    path('register/',views.register,name = "register"),
    path('login/',views.loginUser,name = "login"),
    path('logout/',views.logoutUser,name = "logout"),
    path('profile/<str:username>',views.profile,name = "profile"),
    path('edit_profile/',UserEditView.as_view(),name = "edit_profile"),
    path('password/',PasswordsChangeView.as_view(template_name='change_password.html')),
    path('edit_profile_page/',EditProfilePageView.as_view(), name="edit_profile_page"),
]
