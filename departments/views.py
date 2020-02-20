import requests
import datetime
import copy
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from collections import OrderedDict
from django.db.models import F, Q, Count, Value
from dateutil import parser
from django.utils import timezone
from django.utils.timezone import make_aware
from datetime import timedelta
from . models import EmployeeData, HrCasesData, ProductionStaff, RecruitingCosts2018, SalaryGrid2019, TimeToFill5Yrs, WorkSiteLocations
from accounts.models import HRTeamUser

				


def home(request):
	if request.user.is_authenticated:
		return HttpResponseRedirect('dashboard')
	else: 
		return render(request, 'departments/home.html')
	

@login_required
def dashboard(request):
	currDT = datetime.datetime.now()
	currentDateStr = currDT.strftime("%a, %b %d, %Y")	
	year = currDT.year
	month = currDT.month
	#Set case count start as the first of the month -- dB case statuses are manually updated to "Closed" weekly in order to make case count appear realistic
	monthStartDate = datetime.datetime(year, month, 1)	
	endDate = datetime.date.today()
	yearStartDate = datetime.datetime(year, 1, 1)
	#Set Tier 1 SLA max time period from initial case creation -- 2 days
	twoDaysAgoDT = currDT - datetime.timedelta(days=2)
	twoDaysAgoDate = datetime.datetime(year, month, twoDaysAgoDT.day)		
	#Set Tier 2 SLA max time period from initial case creation -- 4 days
	fourDaysAgoDT = currDT - datetime.timedelta(days=4)	
	fourDaysAgoDate = datetime.datetime(year, month, fourDaysAgoDT.day)	
	#Calculate current total count of all open HR cases for all teams
	allHRCaseCount = HrCasesData.objects.all().exclude(casestatus = 'Closed').filter(datereceived__range=(monthStartDate, endDate)).count()

	if request.user.accesslevel == 'Associate':
		#Determine other dashboard cards case count values pertaining to associates
		userCaseCount = HrCasesData.objects.filter(Q(caseowner=request.user) & Q(datereceived__range=(monthStartDate, endDate))).exclude(casestatus = 'Closed').count()
		teamCaseCount = HrCasesData.objects.filter(Q(casetype=request.user.hrgroup) & Q(datereceived__range=(monthStartDate, endDate))).exclude(casestatus = 'Closed').count()
		teamYTDCaseCount = HrCasesData.objects.filter(Q(casetype=request.user.hrgroup) & Q(datereceived__range=(yearStartDate, endDate))).count()
		cardValuesA = [userCaseCount, teamCaseCount, allHRCaseCount, teamYTDCaseCount]			
		#Determine the total of open cases out of SLA for both Tier 1 and Tier 2 from the user's team
		teamT1OldCaseCount = HrCasesData.objects.filter(Q(casetype=request.user.hrgroup) & Q(casestatus='Open') & Q(datereceived__range=(monthStartDate, twoDaysAgoDate))).count()		
		teamT2OldCaseCount = HrCasesData.objects.filter(Q(casetype=request.user.hrgroup) & Q(casestatus='Escalated') & Q(datereceived__range=(monthStartDate, fourDaysAgoDate))).count()
		teamOldCaseTotal = teamT1OldCaseCount + teamT2OldCaseCount
		#Get user tier level
		userInfo = HRTeamUser.objects.get(userid__exact = request.user)		
		tierGroup = userInfo.get_short_job_title()		
		#Get team good SLA percentage of cases
		if teamCaseCount == 0:
			teamGoodSLAPercentage = 100
		else:
			teamGoodSLAPercentage = 100-round((teamOldCaseTotal/teamCaseCount)*100)
		#Get user good SLA percentage of cases
		if userCaseCount == 0:
			userGoodSLAPercentage = 100
		else:
			if tierGroup == 'Human Resources Operations Specialist I':
				userOldCaseCount = HrCasesData.objects.filter(Q(caseowner=request.user) & Q(casestatus='Open') & Q(datereceived__range=(monthStartDate, twoDaysAgoDate))).count()		
			else:	
				userOldCaseCount = HrCasesData.objects.filter(Q(caseowner=request.user) & Q(casestatus='Escalated') & Q(datereceived__range=(monthStartDate, fourDaysAgoDate))).count()
			userGoodSLAPercentage = 100-round((userOldCaseCount/userCaseCount)*100)		
		#Pass percentages as an array for gauge charts
		gaugeValuesA = [userGoodSLAPercentage, teamGoodSLAPercentage]		
		context = {"currentDate":currentDateStr,"dashboard_page":"active","gaugeValues":gaugeValuesA,"cardValues":cardValuesA}
		return render(request, 'departments/dashboardA.html', context)
		
	else:
		gaugeValuesB = [83,64,92,50,95]			
		context = {"currentDate":currentDateStr,"dashboard_page":"active","gaugeValues":gaugeValuesB}	
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

