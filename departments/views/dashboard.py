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
from departments.models import HrCasesData
from accounts.models import HRTeamUser

				


def home(request):
	if request.user.is_authenticated:
		return HttpResponseRedirect('dashboard')
	else: 
		return render(request, 'departments/home.html')
	

@login_required
def dashboard(request):
	#Get current date info
	currDT = datetime.datetime.now()
	currentDateStr = currDT.strftime("%a, %b %d, %Y")	
	year = currDT.year
	
	#Set the case count start and end dates
	#***For this app, case statuses are manually updated weekly in the database to "Closed" in order to make case count appear realistic***
	startDate = (currDT - datetime.timedelta(days=30)).date()
	endDate = datetime.date.today()
	yearStartDate = datetime.datetime(year, 1, 1)
	
	#Set Tier 1 SLA max time period from initial case creation -- 2 days
	twoDaysAgoDate = (currDT - datetime.timedelta(days=2)).date()	
	
	#Set Tier 2 SLA max time period from initial case creation -- 4 days	
	fourDaysAgoDate = (currDT - datetime.timedelta(days=4)).date()
	
	#Calculate current total count of all open HR cases for all teams
	allHRCaseCount = HrCasesData.allHRCasesTotal.filter_count(startDate, endDate)
	
	#Set team string variables
	attrRet = 'Attrition & Retention'
	beneComp = 'Benefits & Compensation'
	emplRel = 'Employee Relations'
	recrSel = 'Recruitment & Selection'
	trainDev = 'Training & Development'

	#If the user is an Associate...
	if request.user.accesslevel == 'Associate':
		#Get user-specific info
		user = request.user
		team = request.user.hrgroup
		userInfo = HRTeamUser.objects.get(userid__exact = user)		
		tierGroup = userInfo.get_short_job_title()
		
		#Determine other dashboard case count values pertaining to associates		
		userCaseCount = HrCasesData.userCasesTotal.filter_count(user, startDate, endDate)
		teamCaseCount = HrCasesData.teamCasesTotal.filter_count(team, startDate, endDate)
		
		#Determine the total of all open cases for each tier of the user's team separately 
		teamT1CaseCount = HrCasesData.teamTierCasesTotal.filter_count(team, 'Open', startDate, endDate)
		teamT2CaseCount = HrCasesData.teamTierCasesTotal.filter_count(team, 'Escalated', startDate, endDate)
		
		#Determine the total of open cases out of SLA for both Tier 1 and Tier 2 from the user's team
		teamT1OldCaseCount = HrCasesData.teamTierCasesTotal.filter_count(team, 'Open', startDate, twoDaysAgoDate)	
		teamT2OldCaseCount = HrCasesData.teamTierCasesTotal.filter_count(team, 'Open', startDate, fourDaysAgoDate)
		teamOldCaseTotal = teamT1OldCaseCount + teamT2OldCaseCount
		
		#Get team good SLA percentage of cases
		if teamCaseCount == 0:
			teamGoodSLAPercentage = 100
		else:
			teamGoodSLAPercentage = HrCasesData.get_percentage(teamOldCaseTotal, teamCaseCount)
			
		#Get user good SLA percentage of cases
		if userCaseCount == 0:
			userGoodSLAPercentage = 100
		else:
			if tierGroup == 'Human Resources Operations Specialist I':		
				userOldCaseCount = HrCasesData.userOldCasesTotal.filter_count(user, 'Open', startDate, twoDaysAgoDate)
			else:	
				userOldCaseCount = HrCasesData.userOldCasesTotal.filter_count(user, 'Escalated', startDate, fourDaysAgoDate)
			userGoodSLAPercentage = HrCasesData.get_percentage(userOldCaseCount, userCaseCount)

		#Get team satisfaction score info
		scores = HrCasesData.teamScores.score_count(team, yearStartDate, endDate)
		
		#Pass calculated values as arrays
		cardValuesA = [userCaseCount, teamCaseCount, allHRCaseCount]
		tierValuesA = [teamT1CaseCount, teamT2CaseCount]
		gaugeValuesA = [userGoodSLAPercentage, teamGoodSLAPercentage]
		scoreValuesA = [scores['0 - Unknown'],scores['1 - Unsatisfied'],scores['2 - Satisfied'],scores['3 - Highly satisfied']]
		
		context = {"currentDate":currentDateStr,"dashboard_page":"active","scoreValues":scoreValuesA,"tierValues":tierValuesA,"gaugeValues":gaugeValuesA,"cardValues":cardValuesA}
		return render(request, 'departments/dashboardA.html', context)

	#Else, the user is a member of management/IT Admin...
	else:
		#Count all open cases out of SLA for Tier 1 of each team
		attrRetTeamT1OldCaseCount = HrCasesData.teamTierCasesTotal.filter_count(attrRet, 'Open', startDate, twoDaysAgoDate)
		beneCompTeamT1OldCaseCount = HrCasesData.teamTierCasesTotal.filter_count(beneComp, 'Open', startDate, twoDaysAgoDate)
		emplRelTeamT1OldCaseCount = HrCasesData.teamTierCasesTotal.filter_count(emplRel, 'Open', startDate, twoDaysAgoDate)
		recrSelTeamT1OldCaseCount = HrCasesData.teamTierCasesTotal.filter_count(recrSel, 'Open', startDate, twoDaysAgoDate)
		trainDevTeamT1OldCaseCount = HrCasesData.teamTierCasesTotal.filter_count(trainDev, 'Open', startDate, twoDaysAgoDate)	
		
		#Count all open cases out of SLA for Tier 2 of each team
		attrRetTeamT2OldCaseCount = HrCasesData.teamTierCasesTotal.filter_count(attrRet, 'Escalated', startDate, fourDaysAgoDate)
		beneCompTeamT2OldCaseCount = HrCasesData.teamTierCasesTotal.filter_count(beneComp, 'Escalated', startDate, fourDaysAgoDate)
		emplRelTeamT2OldCaseCount = HrCasesData.teamTierCasesTotal.filter_count(emplRel, 'Escalated', startDate, fourDaysAgoDate)
		recrSelTeamT2OldCaseCount = HrCasesData.teamTierCasesTotal.filter_count(recrSel, 'Escalated', startDate, fourDaysAgoDate)
		trainDevTeamT2OldCaseCount = HrCasesData.teamTierCasesTotal.filter_count(trainDev, 'Escalated', startDate, fourDaysAgoDate)
		
		#Calculate the total of open cases out of SLA for both Tiers on each team
		attrRetTeamOldCaseTotal = attrRetTeamT1OldCaseCount + attrRetTeamT2OldCaseCount
		beneCompTeamOldCaseTotal = beneCompTeamT1OldCaseCount + beneCompTeamT2OldCaseCount
		emplRelTeamOldCaseTotal = emplRelTeamT1OldCaseCount + emplRelTeamT2OldCaseCount
		recrSelTeamOldCaseTotal = recrSelTeamT1OldCaseCount + recrSelTeamT2OldCaseCount
		trainDevTeamOldCaseTotal = trainDevTeamT1OldCaseCount + trainDevTeamT2OldCaseCount
		
		#Determine the total of all open Tier 1 cases per team
		attrRetTeamT1CaseCount = HrCasesData.teamTierCasesTotal.filter_count(attrRet, 'Open', startDate, endDate)
		beneCompTeamT1CaseCount = HrCasesData.teamTierCasesTotal.filter_count(beneComp, 'Open', startDate, endDate)
		emplRelTeamT1CaseCount = HrCasesData.teamTierCasesTotal.filter_count(emplRel, 'Open', startDate, endDate)
		recrSelTeamT1CaseCount = HrCasesData.teamTierCasesTotal.filter_count(recrSel, 'Open', startDate, endDate)
		trainDevTeamT1CaseCount = HrCasesData.teamTierCasesTotal.filter_count(trainDev, 'Open', startDate, endDate)
		
		#Determine the total of all open Tier 2 cases per team
		attrRetTeamT2CaseCount = HrCasesData.teamTierCasesTotal.filter_count(attrRet, 'Escalated', startDate, endDate)
		beneCompTeamT2CaseCount = HrCasesData.teamTierCasesTotal.filter_count(beneComp, 'Escalated', startDate, endDate)
		emplRelTeamT2CaseCount = HrCasesData.teamTierCasesTotal.filter_count(emplRel, 'Escalated', startDate, endDate)
		recrSelTeamT2CaseCount = HrCasesData.teamTierCasesTotal.filter_count(recrSel, 'Escalated', startDate, endDate)
		trainDevTeamT2CaseCount = HrCasesData.teamTierCasesTotal.filter_count(trainDev, 'Escalated', startDate, endDate)		
		
		#Calculate the total of all open cases per team including both Tiers
		attrRetTeamCaseCount = attrRetTeamT1CaseCount + attrRetTeamT2CaseCount
		beneCompTeamCaseCount = beneCompTeamT1CaseCount + beneCompTeamT2CaseCount
		emplRelTeamCaseCount = emplRelTeamT1CaseCount + emplRelTeamT2CaseCount
		recrSelTeamCaseCount = recrSelTeamT1CaseCount + recrSelTeamT2CaseCount
		trainDevTeamCaseCount = trainDevTeamT1CaseCount + trainDevTeamT2CaseCount		
		
		#Calculate each team's good SLA percentage of cases
		if attrRetTeamCaseCount == 0:
			attrRetTeamGoodSLAPercentage = 100
		else:
			attrRetTeamGoodSLAPercentage = HrCasesData.get_percentage(attrRetTeamOldCaseTotal, attrRetTeamCaseCount)
		if beneCompTeamCaseCount == 0:
			beneCompTeamGoodSLAPercentage = 100
		else:
			beneCompTeamGoodSLAPercentage = HrCasesData.get_percentage(beneCompTeamOldCaseTotal, beneCompTeamCaseCount)
		if emplRelTeamCaseCount == 0:
			emplRelTeamGoodSLAPercentage = 100
		else:
			emplRelTeamGoodSLAPercentage = HrCasesData.get_percentage(emplRelTeamOldCaseTotal, emplRelTeamCaseCount)
		if recrSelTeamCaseCount == 0:
			recrSelTeamGoodSLAPercentage = 100
		else:
			recrSelTeamGoodSLAPercentage = HrCasesData.get_percentage(recrSelTeamOldCaseTotal, recrSelTeamCaseCount)
		if trainDevTeamCaseCount == 0:
			trainDevTeamGoodSLAPercentage = 100
		else:
			trainDevTeamGoodSLAPercentage = HrCasesData.get_percentage(trainDevTeamOldCaseTotal, trainDevTeamCaseCount)	
			
		#Get satisfaction scores data for all teams
		scoreValuesB = HrCasesData.allTeamsScores.score_count(yearStartDate, endDate)
		
		#Pass all other determined values as arrays
		tier1Values = [attrRetTeamT1CaseCount, beneCompTeamT1CaseCount, emplRelTeamT1CaseCount, recrSelTeamT1CaseCount, trainDevTeamT1CaseCount]
		tier2Values = [attrRetTeamT2CaseCount, beneCompTeamT2CaseCount, emplRelTeamT2CaseCount, recrSelTeamT2CaseCount, trainDevTeamT2CaseCount]
		tierTotalValues = [attrRetTeamCaseCount, beneCompTeamCaseCount, emplRelTeamCaseCount, recrSelTeamCaseCount, trainDevTeamCaseCount]
		gaugeValuesB = [attrRetTeamGoodSLAPercentage, beneCompTeamGoodSLAPercentage, emplRelTeamGoodSLAPercentage, recrSelTeamGoodSLAPercentage, trainDevTeamGoodSLAPercentage]	
		
		
		#TESTING
		#print(list(HrCasesData.allTeamsCasesTotal.filter_count(startDate, endDate)))
		#print(list(HrCasesData.allTeamsTierCasesTotal.filter_count('Open', startDate, endDate)))
		#print(list(HrCasesData.allTeamsTierCasesTotal.filter_count('Escalated', startDate, endDate)))			
		#print(list(HrCasesData.allTeamsTierCasesTotal.filter_count('Open', startDate, twoDaysAgoDate)))
		#print(list(HrCasesData.allTeamsTierCasesTotal.filter_count('Escalated', startDate, fourDaysAgoDate)))
			
		context = {"currentDate":currentDateStr,"dashboard_page":"active","tier1Values":tier1Values,"tier2Values":tier2Values,"tierTotalValues":tierTotalValues,"gaugeValues":gaugeValuesB, "scoreValues":scoreValuesB}	
		return render(request, 'departments/dashboardB.html', context)

