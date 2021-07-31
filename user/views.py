from user.models import Profile
from django.contrib import auth
from django.shortcuts import get_object_or_404, render,redirect,reverse
from .forms import RegisterForm,LoginForm,UpdateForm,ProfilePageUpdateForm
from django.contrib.auth.models import User
from django.contrib.auth import login,authenticate,logout
from django.contrib import messages
from django.views import generic
from django.urls import reverse_lazy
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth.forms import PasswordChangeForm
from django.views.generic import DetailView

# Create your views here.

def register(request):
    
    form = RegisterForm(request.POST or None)

    if form.is_valid():
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")

        newUser = User(username = username)
        newUser.set_password(password)

        newUser.save()
        login(request,newUser)

        messages.info(request,"Başarıyla kayıt oldunuz...")
        return redirect("index")
    context = {
            "form" : form
        }
    return render(request,"register.html",context)

def loginUser(request):
    form = LoginForm(request.POST or None)    
    context = {
        "form" : form
    }
    if form.is_valid():
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")

        user = authenticate(username = username,password = password)

        if user is None:
            messages.info(request,"Kullanıcı adı veya parola hatalı.")
            return render(request,"login.html",context)
        messages.success(request,"Başarıyla giriş yaptınız.")

        login(request,user)

        return redirect("index")
    return render(request,"login.html",context)

def logoutUser(request):
    logout(request)
    messages.success(request,"Başarıyla çıkış yaptınız.")
    return redirect("index")

def profile(request,username):
    user = get_object_or_404(User,username = username)
    return render(request,"profile.html",{"user":user})

"""def edit_profile(request, username):
    user = User(username=username)
    form = UpdateForm(request.POST or None) #request.FILES or None

    if form.is_valid():
        name = form.cleaned_data.get("name")
        surname = form.cleaned_data.get("surname")
        email = form.cleaned_data.get("email")
        profile_photo = form.cleaned_data.get("profile_photo")

        context2 = [name,surname,email]

        for i in context2:
            if i:
                user.i = i
            else:
                continue
        

        messages.info(request,"Başarıyla profiliniz değiştirildi..")
        return redirect(reverse("user:profile",kwargs={"username":username}))
    context = {
            "form" : form
        }
    return render(request,"edit_profile.html",context)"""

class UserEditView(generic.UpdateView):
    form_class = UpdateForm
    template_name = "edit_profile.html"
    success_url = reverse_lazy('index')

    def get_object(self):
        return self.request.user

class PasswordsChangeView(PasswordChangeView):
    form_class = PasswordChangeForm
    success_url = reverse_lazy('index')

class EditProfilePageView(generic.UpdateView):
    form_class = ProfilePageUpdateForm
    template_name = "edit_profile_page.html"
    success_url = reverse_lazy('index')
    
    def get_object(self):
        return self.request.user

