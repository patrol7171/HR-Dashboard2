from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib import auth
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from .forms import ProfileUpdateForm



def login(request):
    if request.method == 'POST':
        user = authenticate(request, username=request.POST['userid'], password = request.POST['password'])
        if user is not None:
            auth.login(request, user)           
            return redirect('dashboard')
        else:
            return render(request, 'accounts/login.html',{'error':'Username and/or password is incorrect.'})
    else:
        return render(request, 'accounts/login.html')


def logout(request):
    #TEMPORARY
    return render(request, 'accounts/home.html')


@login_required
def profile(request):
    if request.method == 'POST':
        p_form = ProfileUpdateForm(request.POST,
                                   request.FILES,
                                   instance=request.user.profile)
        if p_form.is_valid():
            p_form.save()
            messages.success(request, f'Your profile has been updated!')
            return redirect('dashboard')
    else:
        p_form = ProfileUpdateForm(instance=request.user.profile)
        
    context = {
        'p_form': p_form
    }
    return render(request, 'accounts/profile.html', context)
