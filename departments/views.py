from django.shortcuts import render
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from collections import OrderedDict
import requests
import copy
import datetime



def home(request):
	if request.user.is_authenticated:
		return HttpResponseRedirect('dashboard')
	else: 
		return render(request, 'departments/home.html')
	

@login_required
def dashboard(request):
	currentDT = datetime.datetime.now()
	#TESTING
	print (currentDT.strftime("%Y-%m-%d %H:%M:%S"))
	print (currentDT.strftime("%Y/%m/%d"))
	print (currentDT.strftime("%H:%M:%S"))
	print (currentDT.strftime("%I:%M:%S %p"))
	print (currentDT.strftime("%a, %b %d, %Y"))
	
	#Gauge chart values are passed as an array--plugged in sample numbers
	if request.user.accesslevel == 'Associate':
		gaugeValuesA = [92,77]		
		context = {"dashboard_page": "active","gaugeValues": gaugeValuesA}
		return render(request, 'departments/dashboardA.html', context)
	else:
		gaugeValuesB = [83,64,92,50,95]	
		context = {"dashboard_page": "active","gaugeValues": gaugeValuesB}	
		return render(request, 'departments/dashboardB.html', context)


@login_required
def attrition(request):
    context = {"attrition_page": "active"}
    return render(request, 'departments/attrition.html', context)


@login_required
def compensation(request):
	context = {"compensation_page": "active"}
	return render(request, 'departments/compensation.html', context)


@login_required
def recruitment(request):
	context = {"recruitment_page": "active"}
	return render(request, 'departments/recruitment.html', context)


@login_required
def relations(request):
	context = {"relations_page": "active"}
	return render(request, 'departments/relations.html', context)


@login_required
def talent(request):
	context = {"talent_page": "active"}
	return render(request, 'departments/talent.html', context)



@login_required
def demographics(request):	
	context = {"demographics_page":"active","jobaid_menu":"active"}
	return render(request, 'departments/demographics.html', context)
	

@login_required
def locater(request):
	context = {"locater_page":"active","jobaid_menu":"active"}
	return render(request, 'departments/locater.html', context)


@login_required
def policies(request):
	context = {"policies_page":"active","jobaid_menu":"active"}
	return render(request, 'departments/policies.html', context)

