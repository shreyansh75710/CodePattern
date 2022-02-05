from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as djlogin, logout as djlogout
from django.contrib import messages
from django.contrib.auth.decorators import login_required

def login(request):
    if request.user.is_authenticated :
        return redirect('index')
    if request.method=='POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        try:
            user = User.objects.get(username = username)
        except:
            messages.add_message(request, messages.ERROR, 'User does not exists')
        user = authenticate(request, username=username, password=password) # returns user or None
        if user is not None:
            djlogin(request, user)
            messages.add_message(request, messages.SUCCESS, 'User logged in successfully')
            return redirect('index')
        else:
            messages.add_message(request, messages.ERROR, "Incorrect password")
    return render(request, 'auth/login.html')

def register(request):
    form = UserCreationForm()
    if request.method== 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False) # instance will not be created, we can add more data
            user.save() #now instance will be created
            djlogin(request, user) # creates a login session
            messages.add_message(request, messages.SUCCESS, 'User created successfully')
            return redirect('index')
    return render(request, 'auth/register.html', {'form':form})
            

@login_required
def logout(request):
    djlogout(request)
    return redirect('index')