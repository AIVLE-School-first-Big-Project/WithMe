from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    if request.user.is_authenticated:
        return main(request)
    return render(request, "main/base_intro.html")

@login_required
def main(request):
    return render(request, "main/base_test.html")

@login_required
def settings(request):
    return render(request, "main/settings.html")