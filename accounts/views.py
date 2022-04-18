from django.shortcuts import render
from django.http import HttpResponse


def login_ok(request):
    return HttpResponse('\
                        login successful!</br>\
                        <a href="/accounts/logout/">[ Logout ] </a>\
                        ')