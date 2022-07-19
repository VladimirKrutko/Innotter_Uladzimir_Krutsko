from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import CreateView, ListView, DetailView


def log_in(request):
    return HttpResponse('Log in')
