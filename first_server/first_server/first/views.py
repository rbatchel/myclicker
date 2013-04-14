from django.http import HttpResponse
from django.shortcuts import render

#include model import and functions

def hi(request):
	return HttpResponse("Hi world")
