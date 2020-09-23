import requests
import datetime
import copy
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import generic, View
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from collections import OrderedDict, defaultdict
from django.db.models import F, Q, Count, Value
from dateutil import parser
from django.utils import timezone
from django.utils.timezone import make_aware
from datetime import timedelta
from departments.models import EmployeeData, HrCasesData, RecruitingCosts2019, SalaryGrid2020, WorkSiteLocations
from accounts.models import HRTeamUser




#Get current date info
currDT = datetime.datetime.now()
currentDateStr = currDT.strftime("%a, %b %d, %Y")	
year = currDT.year

#Set the case count start and end dates
##*** For this app, case statuses are manually updated weekly in the database to "Closed" in order to make the case status counts appear realistic ***
startDate = currDT - datetime.timedelta(days=30)
endDate = currDT 
yearStartDate = datetime.datetime(year, 1, 1)

#Set Tier 1 SLA max time period from initial case creation -- 2 days
twoDaysAgoDate = currDT - datetime.timedelta(days=2)	

#Set Tier 2 SLA max time period from initial case creation -- 4 days	
fourDaysAgoDate = currDT - datetime.timedelta(days=4)

#Set team string variables
attrRet = 'Attrition & Retention'
beneComp = 'Benefits & Compensation'
emplRel = 'Employee Relations'
recrSel = 'Recruitment & Selection'
trainDev = 'Training & Development'


@login_required
def attrition(request, tabnum):
    global attrRet
    activeTab = getTabType(tabnum)
    casework_data = getCaseworkInfo(attrRet,request)
    cssurvey_data = getCSSurveyInfo(attrRet)
    rft = EmployeeData.rftCount.rft_count()
    rft_info = [list(rft.keys()),list(rft.values())]    
    rft_raceCount = EmployeeData.rftCountByRace.rftRace_count()
    rft_genderCount = EmployeeData.rftCountByGender.rftGender_count()
            
    context = {"attrition_page":"active","dept_menu":"active",activeTab:"active",
    "requestor_list":casework_data[0],"priority_list":casework_data[1],"case_list":casework_data[2],"case_avg":casework_data[3],
    "scores_info":cssurvey_data[0],"dissatisfied_info":cssurvey_data[1],"unknown_info":cssurvey_data[2],
    "rft_info":rft_info,"rft_raceCount":rft_raceCount,"rft_genderCount":rft_genderCount}   
    
    return render(request, 'departments/attrition.html', context)


@login_required
def compensation(request, tabnum):
    global beneComp
    activeTab = getTabType(tabnum)
    casework_data = getCaseworkInfo(beneComp,request)
    cssurvey_data = getCSSurveyInfo(beneComp)
    payDistrib_dept = EmployeeData.hourlyPayDistribByDept.pay_distrib()
    payDistrib_gender = EmployeeData.hourlyPayDistribByGender.pay_distrib()
    payDistrib_race = EmployeeData.hourlyPayDistribByRace.pay_distrib()
    
    context = {"compensation_page":"active","dept_menu":"active",activeTab:"active",
    "requestor_list":casework_data[0],"priority_list":casework_data[1],"case_list":casework_data[2],"case_avg":casework_data[3],
    "scores_info":cssurvey_data[0],"dissatisfied_info":cssurvey_data[1],"unknown_info":cssurvey_data[2],
    "payDistrib_dept":payDistrib_dept,"payDistrib_gender":payDistrib_gender,"payDistrib_race":payDistrib_race}
    
    return render(request, 'departments/compensation.html', context)


@login_required
def recruitment(request, tabnum):
    global recrSel
    activeTab = getTabType(tabnum)
    casework_data = getCaseworkInfo(recrSel,request)
    cssurvey_data = getCSSurveyInfo(recrSel)    
    rec2019_costs = RecruitingCosts2019.recruit2019Costs.costs()
    preHireEmpSource_counts = EmployeeData.preHireEmpSourceCount.sources()

    context = {"recruitment_page":"active","dept_menu":"active",activeTab:"active",
    "requestor_list":casework_data[0],"priority_list":casework_data[1],"case_list":casework_data[2],"case_avg":casework_data[3],
    "scores_info":cssurvey_data[0],"dissatisfied_info":cssurvey_data[1],"unknown_info":cssurvey_data[2],
    "rec2019_costs":rec2019_costs,"preHireEmpSource_counts":preHireEmpSource_counts}
    
    return render(request, 'departments/recruitment.html', context)


@login_required
def relations(request, tabnum):
    global emplRel
    activeTab = getTabType(tabnum)   
    casework_data = getCaseworkInfo(emplRel,request)
    cssurvey_data = getCSSurveyInfo(emplRel)   
    engSurvey_results = EmployeeData.engageSurveyResultsByDept.dept_results()
    empSatSurvey_results = EmployeeData.empSatSurveyResultsByDept.dept_results()

    context = {"relations_page":"active","dept_menu":"active",activeTab:"active",
    "requestor_list":casework_data[0],"priority_list":casework_data[1],"case_list":casework_data[2],"case_avg":casework_data[3],
    "scores_info":cssurvey_data[0],"dissatisfied_info":cssurvey_data[1],"unknown_info":cssurvey_data[2],
    "engSurvey_results":engSurvey_results,"empSatSurvey_results":empSatSurvey_results}
    
    return render(request, 'departments/relations.html', context)


@login_required
def talent(request, tabnum):
    global trainDev
    activeTab = getTabType(tabnum)
    casework_data = getCaseworkInfo(trainDev,request)
    cssurvey_data = getCSSurveyInfo(trainDev)
    perfScore_count = EmployeeData.perfScoreCount.perf_scores()
    perfScoreByDept_count = EmployeeData.perfScoreByDeptCount.perf_scores()

    context = {"talent_page":"active","dept_menu":"active",activeTab:"active",
    "requestor_list":casework_data[0],"priority_list":casework_data[1],"case_list":casework_data[2],"case_avg":casework_data[3],
    "scores_info":cssurvey_data[0],"dissatisfied_info":cssurvey_data[1],"unknown_info":cssurvey_data[2],
    "perfScore_count":perfScore_count,"perfScoreByDept_count":perfScoreByDept_count}
    
    return render(request, 'departments/talent.html', context)


def getTabType(num):
    if num == 1:
        tab = "casework_tab"
    elif num == 2:
        tab = "cssurveys_tab"       
    else:
        tab = "teamdata_tab" 
    return tab


def getCaseworkInfo(team,request):
    requestor_list = getYTDCaseRequestorList(team)
    priority_list = getYTDCasePriorityList(team)
    case_list = getOpenCasesListInfo(team,request)
    case_avg = getAvgCaseCloseNumByMonth(team)   
    return requestor_list, priority_list, case_list, case_avg


def getCSSurveyInfo(team):
    scores_info = getYearlySurveyScoreResults(team)
    dissatisfied_info = getYearlyScoreTypeByRequestor(team,'1 - Unsatisfied')
    unknown_info = getYearlyScoreTypeByRequestor(team,'0 - Unknown')
    return scores_info, dissatisfied_info, unknown_info


def getYTDCaseRequestorList(team):
    global yearStartDate, endDate
    list = HrCasesData.teamRequestTypeCaseTotals.type_count(team, yearStartDate, endDate)
    return list
    

def getYTDCasePriorityList(team):
    global yearStartDate, endDate
    list = HrCasesData.teamPriorityLevelCaseTotals.level_count(team, yearStartDate, endDate)
    return list


def getOpenCasesListInfo(team,request):
    global startDate, endDate
    list = HrCasesData.teamOpenCasesList.case_list(team, startDate, endDate)   
    page = request.GET.get('page', 1)
    paginator = Paginator(list, 8)
    try:
        list = paginator.page(page)
    except PageNotAnInteger:
        list = paginator.page(1)
    except EmptyPage:
        list = paginator.page(paginator.num_pages)
    return list


def getAvgCaseCloseNumByMonth(team):
    global yearStartDate, endDate
    result = HrCasesData.teamCurrAvgCaseCloseNumByMonth.avg_count(team, yearStartDate, endDate)
    return result


def getYearlySurveyScoreResults(team):
    global year, endDate, currDT
    scoreYearList = [currDT.year-1, currDT.year-2, currDT.year-3, currDT.year-4]
    yearStartList = [datetime.datetime(year-1,1,1), datetime.datetime(year-2,1,1), datetime.datetime(year-3,1,1), datetime.datetime(year-4,1,1)] 
    yearEndList = [datetime.datetime(year-1,12,31), datetime.datetime(year-2,12,31), datetime.datetime(year-3,12,31), datetime.datetime(year-4,12,31)] 
    scoresDict = {}
    for a, b, c in zip(scoreYearList, yearStartList, yearEndList): 
        scoresDict[a] = HrCasesData.teamScores.score_count(team, b, c)
    return scoresDict  


def getYearlyScoreTypeByRequestor(team, scoreType):
    global year, yearStartDate, endDate, currDT
    scoreYearList = [currDT.year, currDT.year-1, currDT.year-2, currDT.year-3, currDT.year-4]
    yearStartList = [yearStartDate, datetime.datetime(year-1,1,1), datetime.datetime(year-2,1,1), datetime.datetime(year-3,1,1), datetime.datetime(year-4,1,1)] 
    yearEndList = [endDate, datetime.datetime(year-1,12,31), datetime.datetime(year-2,12,31), datetime.datetime(year-3,12,31), datetime.datetime(year-4,12,31)] 
    requestorDict = {}
    for a, b, c in zip(scoreYearList, yearStartList, yearEndList): 
        requestorDict[a] = HrCasesData.teamScoreCountByRequestor.requestor_count(team, scoreType, b, c)
    return requestorDict


