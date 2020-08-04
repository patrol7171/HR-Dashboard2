import requests
import datetime
import pytz
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import generic, View
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from dateutil import parser
from django.utils import timezone
from django.utils.timezone import make_aware
from datetime import timedelta
from departments.models import HrCasesData
from accounts.models import HRTeamUser

				



#Set tier level statuses globally
status1 = 'Open'
status2 = 'Escalated'


def welcome(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('dashboard')
    else:    
        return render(request, 'departments/welcome.html')


def home(request):
	if request.user.is_authenticated:
		return HttpResponseRedirect('dashboard')
	else: 
		context = {"home_page":"active"}
		return render(request, 'departments/home.html', context)


def about(request):
	context = {"about_page":"active"}
	return render(request, 'departments/about.html', context)
	

@login_required
def dashboard(request):
    global status1, status2
    #Set current date with local time zone
    currDT = (datetime.datetime.now()).replace(tzinfo=pytz.utc)
    currentDateStr = currDT.strftime("%a, %b %d, %Y")

    #Set Tier 1 SLA max time period from initial case creation -- 2 days
    twoDaysAgoDate = currDT - datetime.timedelta(days=2)

    #Set Tier 2 SLA max time period from initial case creation -- 4 days	
    fourDaysAgoDate = currDT - datetime.timedelta(days=4)

    #Set the case count start and end dates
    #***For this app, case statuses are manually updated weekly in the database to "Closed" in order to make case count appear realistic***
    #***Case dates extend out to Jan 2024 to allow this app to run with case data up to that date; start date is 30 days prior to the current date***
    startDate = currDT - datetime.timedelta(days=30)
    endDate = currDT 

    #Set current year		
    year = currDT.year
    yearStartDate = datetime.datetime(year, 1, 1)

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
        teamT1CaseCount = get_case_total_by_tier(team, status1, startDate, endDate)
        teamT2CaseCount = get_case_total_by_tier(team, status2, startDate, endDate)

        #Determine the total of open cases out of SLA for both Tier 1 and Tier 2 from the user's team
        teamOldCaseTotal = get_case_total_by_SLA(team, startDate, twoDaysAgoDate, fourDaysAgoDate)

        #Get team good SLA percentage of cases
        teamGoodSLAPercentage = get_SLA_percentage(teamOldCaseTotal, teamCaseCount)
            
        #Get user good SLA percentage of cases
        if tierGroup == 'Human Resources Operations Specialist I':		
            userOldCaseCount = HrCasesData.userOldCasesTotal.filter_count(user, status1, startDate, twoDaysAgoDate)
        else:	
            userOldCaseCount = HrCasesData.userOldCasesTotal.filter_count(user, status2, startDate, fourDaysAgoDate)
        userGoodSLAPercentage = get_SLA_percentage(userOldCaseCount, userCaseCount)

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
        #Calculate the total of open cases out of SLA for both Tiers on each team
        attrRetTeamOldCaseTotal = get_case_total_by_SLA(attrRet, startDate, twoDaysAgoDate, fourDaysAgoDate)
        beneCompTeamOldCaseTotal = get_case_total_by_SLA(beneComp, startDate, twoDaysAgoDate, fourDaysAgoDate)
        emplRelTeamOldCaseTotal = get_case_total_by_SLA(emplRel, startDate, twoDaysAgoDate, fourDaysAgoDate)
        recrSelTeamOldCaseTotal = get_case_total_by_SLA(recrSel, startDate, twoDaysAgoDate, fourDaysAgoDate)
        trainDevTeamOldCaseTotal = get_case_total_by_SLA(trainDev, startDate, twoDaysAgoDate, fourDaysAgoDate)

        #Determine the total of all open Tier 1 cases per team
        attrRetTeamT1CaseCount = get_case_total_by_tier(attrRet, status1, startDate, endDate)
        beneCompTeamT1CaseCount = get_case_total_by_tier(beneComp, status1, startDate, endDate)
        emplRelTeamT1CaseCount = get_case_total_by_tier(emplRel, status1, startDate, endDate)
        recrSelTeamT1CaseCount = get_case_total_by_tier(recrSel, status1, startDate, endDate)
        trainDevTeamT1CaseCount = get_case_total_by_tier(trainDev, status1, startDate, endDate)
        
        #Determine the total of all open Tier 2 cases per team
        attrRetTeamT2CaseCount = get_case_total_by_tier(attrRet, status2, startDate, endDate)
        beneCompTeamT2CaseCount = get_case_total_by_tier(beneComp, status2, startDate, endDate)
        emplRelTeamT2CaseCount = get_case_total_by_tier(emplRel, status2, startDate, endDate)
        recrSelTeamT2CaseCount = get_case_total_by_tier(recrSel, status2, startDate, endDate)
        trainDevTeamT2CaseCount = get_case_total_by_tier(trainDev, status2, startDate, endDate)

        #Calculate the total of all open cases per team including both Tiers
        attrRetTeamCaseCount = attrRetTeamT1CaseCount + attrRetTeamT2CaseCount
        beneCompTeamCaseCount = beneCompTeamT1CaseCount + beneCompTeamT2CaseCount
        emplRelTeamCaseCount = emplRelTeamT1CaseCount + emplRelTeamT2CaseCount
        recrSelTeamCaseCount = recrSelTeamT1CaseCount + recrSelTeamT2CaseCount
        trainDevTeamCaseCount = trainDevTeamT1CaseCount + trainDevTeamT2CaseCount

        #Calculate each team's good SLA percentage of cases
        attrRetTeamGoodSLAPercentage = get_SLA_percentage(attrRetTeamOldCaseTotal, attrRetTeamCaseCount)
        beneCompTeamGoodSLAPercentage = get_SLA_percentage(beneCompTeamOldCaseTotal, beneCompTeamCaseCount)
        emplRelTeamGoodSLAPercentage = get_SLA_percentage(emplRelTeamOldCaseTotal, emplRelTeamCaseCount)
        recrSelTeamGoodSLAPercentage = get_SLA_percentage(recrSelTeamOldCaseTotal, recrSelTeamCaseCount)
        trainDevTeamGoodSLAPercentage = get_SLA_percentage(trainDevTeamOldCaseTotal, trainDevTeamCaseCount)	       
                    
        #Get satisfaction scores data for all teams
        scoreValuesB = HrCasesData.allTeamsScores.score_count(yearStartDate, endDate)

        #Pass all calculated values as arrays
        tier1Values = [attrRetTeamT1CaseCount, beneCompTeamT1CaseCount, emplRelTeamT1CaseCount, recrSelTeamT1CaseCount, trainDevTeamT1CaseCount]
        tier2Values = [attrRetTeamT2CaseCount, beneCompTeamT2CaseCount, emplRelTeamT2CaseCount, recrSelTeamT2CaseCount, trainDevTeamT2CaseCount]
        tierTotalValues = [attrRetTeamCaseCount, beneCompTeamCaseCount, emplRelTeamCaseCount, recrSelTeamCaseCount, trainDevTeamCaseCount]
        gaugeValuesB = [attrRetTeamGoodSLAPercentage, beneCompTeamGoodSLAPercentage, emplRelTeamGoodSLAPercentage, recrSelTeamGoodSLAPercentage, trainDevTeamGoodSLAPercentage]
                    
        context = {"currentDate":currentDateStr,"dashboard_page":"active","tier1Values":tier1Values,"tier2Values":tier2Values,"tierTotalValues":tierTotalValues,"gaugeValues":gaugeValuesB, "scoreValues":scoreValuesB}	
        return render(request, 'departments/dashboardB.html', context)


def get_SLA_percentage(oosla_count, all_count):
    if all_count == 0:
        percent = 100
    else:
        percent = HrCasesData.get_percentage(oosla_count, all_count)
    return percent


def get_case_total_by_SLA(groupType, start, max_SLA1, max_SLA2):
    global status1, status2
    t1_count = HrCasesData.teamTierCasesTotal.filter_count(groupType, status1, start, max_SLA1)
    t2_count = HrCasesData.teamTierCasesTotal.filter_count(groupType, status2, start, max_SLA2)        
    total = t1_count + t2_count
    return total


def get_case_total_by_tier(groupType, status, start, end):
    count = HrCasesData.teamTierCasesTotal.filter_count(groupType, status, start, end)
    return count