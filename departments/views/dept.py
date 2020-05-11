import requests
import datetime
import copy
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import generic, View
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from collections import OrderedDict
from django.db.models import F, Q, Count, Value
from dateutil import parser
from django.utils import timezone
from django.utils.timezone import make_aware
from datetime import timedelta
from departments.models import EmployeeData, HrCasesData, ProductionStaff, RecruitingCosts2018, SalaryGrid2019, TimeToFill5Yrs, WorkSiteLocations
from accounts.models import HRTeamUser




@login_required
def attrition(request):
    context = {"attrition_page": "active", "dept_menu":"active"}
    return render(request, 'departments/attrition.html', context)


@login_required
def compensation(request):
	context = {"compensation_page": "active", "dept_menu":"active"}
	return render(request, 'departments/compensation.html', context)


@login_required
def recruitment(request):
	context = {"recruitment_page": "active", "dept_menu":"active"}
	return render(request, 'departments/recruitment.html', context)


@login_required
def relations(request):
	context = {"relations_page": "active", "dept_menu":"active"}
	return render(request, 'departments/relations.html', context)


@login_required
def talent(request):
	context = {"talent_page": "active", "dept_menu":"active"}
	return render(request, 'departments/talent.html', context)



