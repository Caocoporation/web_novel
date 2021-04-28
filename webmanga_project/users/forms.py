from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile



class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "password-field",
                "id": "password-field"
            }
        )
    ) 

    def clean_username(self):
        username = self.cleaned_data.get("username")
        user = User.objects.filter(username=username)

        if not user.exists():
            raise forms.ValidationError(f"Oops! {username} doesn't exist! Please choose another username.")

        return username

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField()
    
    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "email", "password1", "password2"]
    
    
class UpdateUserForm(forms.ModelForm):
    email = forms.EmailField()
    first_name = forms.CharField(max_length=50, label="First Name")
    last_name = forms.CharField(max_length=50, label="Last Name")
    
    class Meta:
        model = User
        fields = ["first_name", "last_name", "email"]

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ["avatar"]
