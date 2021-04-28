from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from .forms import (
    UserRegistrationForm, UpdateUserForm, 
    ProfileUpdateForm, LoginForm
)
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import Profile
from .utils import delete_junk_image
from django.contrib.auth import  authenticate, login, logout

 
def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST or None)

        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            messages.success(request,  message= f"Account has been created for {username}!")
            return redirect(to="login")

    else:
        form =  UserRegistrationForm()
    
    return render(request, template_name="register.htm", context={"form" : form})

@login_required
def profile(request):
    if request.method == "POST":
        origin_avatar = request.user.profile.avatar.path
        
        u_form = UpdateUserForm(request.POST, instance=request.user)

        p_form = ProfileUpdateForm(
            request.POST, 
            request.FILES, 
            instance=request.user.profile
        )

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()

            if request.FILES.get("avatar"): 
                delete_junk_image(origin_avatar)

            messages.success(request,  message= f"Your Profile Has Been Updated!")
            return redirect(to="user-profile")

    else:
        u_form = UpdateUserForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = { "u_form" : u_form, "p_form" : p_form }
    
    return render(request, template_name="profile.htm", context=context)

