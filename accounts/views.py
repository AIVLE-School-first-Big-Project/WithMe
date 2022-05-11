from django.shortcuts import render, redirect
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth import login as auth_login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import UserType
from django.contrib.auth.views import LoginView
from .forms import SignupForm, CustomAuthenticationForm


class CustomLoginView(LoginView):
    template_name = 'main/index_login.html'
    form_class = CustomAuthenticationForm


login = CustomLoginView.as_view()


def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            signed_user = form.save()
            auth_login(request, signed_user)
            return redirect("service")
    else:
        form = SignupForm()
    return render(request, 'accounts/signup.html', {'form': form})


@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('accounts:Login')  # 나중에 메인페이지로 이동
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'accounts/change_password.html', {
        'form': form
    })


@login_required
def update(request):
    current_user = request.user  # User.objects.get(id = request.session.get('login_session', ''))
    usertype = current_user.User_type  # request.session.get('Type_name')
    # userid = request.session.get('username')
    if request.method == 'POST':
        new_type = str(request.POST.get('new_Type'))
        if usertype != new_type:
            try:
                user_type = UserType.objects.get(Type_name=new_type)
            except UserType.DoesNotExist:
                user_type = None
            user = current_user  # User.objects.get(username = userid)
            user.User_type = user_type
            user.save()

            # user_type.save()

            # messages.info(request, 'type이 변경되었습니다.')

    return render(request, 'accounts/change_type.html')
