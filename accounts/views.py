from django.shortcuts import render, redirect
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse
from .models import User, UserType

def login_ok(request):
    return HttpResponse('\
                        login successful!</br>\
                        <a href="/accounts/logout/">[ Logout ] </a>\
                        ')

def signup(request):
    if request.method == 'POST':
        # Check duplicate account
        if User.objects.filter(email=request.POST['email']).exists():
            return render(request, 'accounts/signup_error_duplicate.html')

        username = request.POST['username']
        raw_password = request.POST['password1']
        password = request.POST['password2']

        # Check Password Typo
        if raw_password != password:
            return render(request, 'accounts/signup_error_password.html')
        email = request.POST['email']
        
        # Check UserType
        try:
            user_type = UserType.objects.get(Type_name = request.POST['user_type'])
        except UserType.DoesNotExist:
            user_type = None

        user = User.objects.create_user(username, email, raw_password)
        user.User_type = user_type
        user.save()
        return redirect('accounts:Login')
    else:
        return render(request, 'accounts/signup_form.html')

@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('accounts:Login') # 나중에 메인페이지로 이동
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'accounts/change_password.html', {
        'form': form
    })