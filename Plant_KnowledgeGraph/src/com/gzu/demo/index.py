# -*- coding: utf-8 -*-
#from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators import csrf
 

def new_index(request):
	context = {}
	return render(request, 'new/index.html', context)
	