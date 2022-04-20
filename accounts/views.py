from django.shortcuts import render, redirect
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