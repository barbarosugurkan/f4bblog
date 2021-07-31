from django import forms
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.models import User
from .models import Profile

class RegisterForm(forms.Form):
    username = forms.CharField(max_length = 50,label = "Kullanıcı Adı")
    password = forms.CharField(max_length = 20,label = "Parola",widget = forms.PasswordInput)
    confirm = forms.CharField(max_length = 20,label = "Parolayı Doğrula",widget = forms.PasswordInput)

    def clean(self):
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")
        confirm = self.cleaned_data.get("confirm")

        if password and confirm and password != confirm:
            raise forms.ValidationError("Parolalar Eşleşmiyor")
        
        values = {
            "username" : username,
            "password" : password
        }
        return values

class LoginForm(forms.Form):
    username = forms.CharField(label = "Kullanıcı Adı")
    password = forms.CharField(label = "Parola",widget = forms.PasswordInput)

class UpdateForm(UserChangeForm):
    email = forms.EmailField(label="E-Posta",required=False,widget = forms.EmailInput(attrs={'class':'form-control'}))
    first_name = forms.CharField(max_length=100,label="İsim",required=False,widget=forms.TextInput(attrs={'class':'form-control'}))
    last_name = forms.CharField(max_length=100,label="Soyisim",required=False,widget=forms.TextInput(attrs={'class':'form-control'}))
    username = forms.CharField(max_length=100,label="Kullanıcı Adı",widget=forms.TextInput(attrs={'class':'form-control'}))
    last_login = forms.CharField(max_length=100,label="Son Giriş Tarihi",widget=forms.TextInput(attrs={'class':'form-control'}))
    is_superuser = forms.CharField(max_length=100,label="Superuser mı?",required=False,widget=forms.CheckboxInput(attrs={'class':'form-check'}))
    is_staff = forms.CharField(max_length=100,label="Staff mı?",required=False,widget=forms.CheckboxInput(attrs={'class':'form-check'}))
    is_active = forms.CharField(max_length=100,label="Aktif mi?",required=False,widget=forms.CheckboxInput(attrs={'class':'form-check'}))
    date_joined = forms.CharField(max_length=100,label="Katılma Tarihi",widget=forms.TextInput(attrs={'class':'form-control'}))

    class Meta:
        model = User
        fields = ('username','first_name','last_name','email','password','last_login','is_superuser','is_staff','is_active','date_joined')

class ProfilePageUpdateForm(UserChangeForm):
    bio = forms.CharField(label="Bio",required=False,widget=forms.Textarea(attrs={'class':'form-control'}))
    profile_pic = forms.FileField(label="Profil Fotosu",required=False,widget=forms.FileInput(attrs={'class':'form-control'}))
    website_url = forms.CharField(label="Website URL",required=False,widget=forms.TextInput(attrs={'class':'form-control'}))
    facebook_url = forms.CharField(label="Facebook URL",required=False,widget=forms.TextInput(attrs={'class':'form-control'}))
    twitter_url = forms.CharField(label="Twitter URL",required=False,widget=forms.TextInput(attrs={'class':'form-control'}))
    instagram_url = forms.CharField(label="Instagram URL",required=False,widget=forms.TextInput(attrs={'class':'form-control'}))
    pinterest_url = forms.CharField(label="Pinterest URL",required=False,widget=forms.TextInput(attrs={'class':'form-control'}))

    class Meta:
        model = Profile
        fields = ('bio', 'profile_pic', 'website_url','facebook_url','twitter_url','instagram_url','pinterest_url')
