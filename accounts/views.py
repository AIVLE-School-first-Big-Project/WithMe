from django.shortcuts import render
from django.http import HttpResponse


def login_ok(request):
    return HttpResponse('<u>login successful!</u>')