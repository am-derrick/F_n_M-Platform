from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from .forms import SignUpForm
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.urls import reverse

def signup(request):
    """sign up/register view"""
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'accounts/signup.html',  {'form': form})

class CustomLoginView(LoginView):
    template_name = 'accounts/login.html'

def custom_logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('login'))

@login_required
def home(request):
    """home view"""
    return redirect('macroeconomics:home')