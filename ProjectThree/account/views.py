from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic import View

from .forms import LogInForm, UserRegistrationForm, UserEditForm, ProfileEditForm
from .models import Profile

def login_view(request):
    template = "account/login.html"

    if request.method == "POST":
        form = LogInForm(request.POST or None)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd['username'], password=cd['password'])

            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponse("Log-In Successful")
                else:
                    return HttpResponse("Account Disabled")
            else:
                return HttpResponse("Invalid Log In")
    else:
        form = LogInForm()


    context = {
        'form': form
    }

    return render(request, template, context)


@login_required
def dashboard(request):
    context = {
        'section' : "dashboard",
    }
    return render(request, 'account/dashboard.html', context)

class RegisterForm(View):

    def get(self, request):
        user_form = UserRegistrationForm()
        context={
            'user_form':user_form,
        }
        return render(request, "account/register.html", context)

    def post(self, request):
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit = False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            profile = Profile.objects.create(user=new_user)
           

        context = {
            'user_form': user_form,
        }

        return render(request, "account/register_done.html", context)


class ProfileEdit(View):

    def get(self, request):
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
        context = {
            'user_form' : user_form,
            'profile_form' : profile_form,
        }
        return render(request, 'account/edit.html', context)

    def post(self, request):
        user_form = UserEditForm(instance=request.user, data=request.POST)
        profile_form = ProfileEditForm(instance=request.user.profile, data=request.POST, files=request.FILES)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Account information updated successfully')
        else:
            user_form = UserEditForm(instance=request.user)
            profile_form = ProfileEditForm(instance=request.user.profile)
            messages.success(request, 'Error in updating your account info')

        context = {
            'user_form' : user_form,
            'profile_form' : profile_form,
        }
        return render(request, 'account/edit.html', context)
