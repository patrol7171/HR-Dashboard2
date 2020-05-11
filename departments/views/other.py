import requests
import datetime
import copy
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import generic, View
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from dateutil import parser
from django.utils import timezone
from django.utils.timezone import make_aware
from datetime import timedelta
from departments.models import EmployeeData, WorkSiteLocations
from accounts.models import HRTeamUser

				

@login_required
def demographics(request):
	status = EmployeeData.empStatusCount.status_count()
	deptCount = EmployeeData.staffDeptCount.dept_count()
	gender = EmployeeData.staffGenderCount.gender_count()
	race = EmployeeData.staffRaceCount.race_count()
	marital = EmployeeData.staffMaritalStatCount.marital_count()
	raceByDeptValues = EmployeeData.staffRaceByDeptCount.filter_count()
	maritalStatByDeptValues = EmployeeData.staffMaritalStatByDeptCount.filter_count()
	age = EmployeeData.staffAgeCount.age_count()
	
	statusValues = [status['Voluntarily Terminated'], status['Terminated for Cause'], status['Active'], status['Future Start'], status['Leave of Absence']]
	deptCountValues = [deptCount['Executive Office'], deptCount['Admin Offices'], deptCount['IT - Information Systems'], deptCount['Production       '], deptCount['Sales'], deptCount['Software Engineering']]
	genderValues = [gender['Male'],gender['Female']]
	raceValues = [race['American Indian or Alaska Native'],race['Asian'],race['Black or African American'],race['Hispanic'],race['Two or more races'],race['White']]
	maritalStatValues = [marital['Divorced'],marital['Married'],marital['Separated'],marital['Single'],marital['Widowed']]
	ageCountValues = [list(age.keys()),list(age.values())]
	
	context = {"demographics_page":"active","statusValues":statusValues,"deptCountValues":deptCountValues,"genderValues":genderValues,"raceValues":raceValues,
	"maritalStatValues":maritalStatValues,"raceByDeptValues":raceByDeptValues,"maritalStatByDeptValues":maritalStatByDeptValues, "ageCountValues":ageCountValues}
	
	return render(request, 'departments/demographics.html', context)
	

@login_required
def locater(request):
	context = {"locater_page":"active","jobaid_menu":"active"}
	
	return render(request, 'departments/locater.html', context)


@login_required
def policies(request):
	context = {"policies_page":"active","jobaid_menu":"active"}
	
	return render(request, 'departments/policies.html', context)