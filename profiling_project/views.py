from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from django.contrib import messages




from . forms import SignUpForm

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            messages.success(request, 'Your password was updated successfully!')  # <-

            return redirect('/dashboard')
    else:
        form = SignUpForm()
        messages.warning(request, 'Please correct the errors below')  # <-
    return render(request, 'registration/signup.html', {'form': form})


def index(request):
    return render(request, 'core/index.html')