from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import SignUpForm
from django.contrib.auth.views import LoginView, LogoutView

def register(request):
    """sign up/register view"""
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('analysis')
    else:
        form = SignUpForm()
    return render(request, 'accounts/register.html',  {'form': form})

class CustomLoginView(LoginView):
    template_name = 'accounts/login.html'

class CustomLogoutView(LogoutView):
    next_page = 'login'


def analysis_view(request):
    return render(request, 'analysis/analysis.html')