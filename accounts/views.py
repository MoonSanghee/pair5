from django.shortcuts import render, redirect
from .models import User
from django.contrib.auth import get_user_model
from .forms import CustomUserCreationForm, CustomUserChangeForm
from django.contrib.auth import login as auth_login

# Create your views here.
def index(request):
    users = get_user_model().objects.all()
    context = {'users' : users}
    return render(request, 'accounts/index.html', context)

def signup(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('accounts:index')
    else:
        form = CustomUserCreationForm()
    context = {'form' : form}
    return render(request, 'accounts/signup.html', context)

def detail(request, user_pk):
    user = get_user_model.objects.get(pk=user_pk)
    context = {'user' : user}
    return render(request, 'accounts/detail.html', context)
          