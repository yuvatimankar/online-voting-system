from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.shortcuts import render, redirect
from django.urls import reverse  


from .forms import UserRegistrationForm

# My  views.

def login_user(request):
    if request.method == "POST":
       username = request.POST.get('username')
       password = request.POST.get('password')
       user = authenticate(request, username=username, password=password)
       if user is not None:
           login(request, user)
           redirect_url = request.GET.get('next', 'polls:home')
#redirect to home
          #return HttpResponseRedirect(reverse('polls:list'))
           return redirect(redirect_url)
       else:
               messages.error(request, 'wrong useername or password')
    return render(request, 'accounts/login.html')

#loging out the user
@login_required
def logout_user(request):
    logout(request)
    # return HttpResponseRedirect(reverse('polls:home'))
    return redirect('polls:home')


#new user registration
def user_registration(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            email    = form.cleaned_data['email']
            user = User.objects.create_user(username, email=email, password=password)
            messages.success(request, 'You  have now registered {}'.format(user.username))
            # return HttpResponseRedirect(reverse('accounts:login'))
            return redirect('accounts:login')
            print('form was valid')
    else:
        form = UserRegistrationForm()
    return render(request, 'accounts/reqister.html', {'form':form})
