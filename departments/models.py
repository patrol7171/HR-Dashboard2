import calendar
import datetime
import pytz
from django.conf import settings
from django.db import models
from django.contrib.auth.models import Group
from django.db.models import F, Q, Count, Value, Avg
from django.contrib.admin.utils import flatten
from collections import OrderedDict, defaultdict
from datetime import date, timedelta
from calendar import month_abbr
from decimal import Decimal
from collections import ChainMap
from accounts.models import HRTeamUser





"""
*************************
*  EMPLOYEE/STAFF DATA  *
*************************
"""
class EmployeeStatusCountManager(models.Manager):
	def status_count(self):
		result = super().get_queryset().values('employmentstatus').annotate(count=Count('employmentstatus'))
		statusList = list(result)
		status_dicts = [{dict['employmentstatus']: dict['count']} for dict in statusList]
		status_counts = {k: v for d in status_dicts for k, v in d.items()}
		return status_counts

class StaffTotalsByDeptManager(models.Manager):
	def dept_count(self):
		result = super().get_queryset().filter(Q(employmentstatus='Active') | Q(employmentstatus='Leave of Absence') | Q(employmentstatus='Future Start')).values('department').annotate(count=Count('department'))
		deptList = list(result)
		dept_dicts = [{dict['department']: dict['count']} for dict in deptList]
		dept_counts = {k: v for d in dept_dicts for k, v in d.items()}
		return dept_counts

class StaffGenderCountManager(models.Manager):
	def gender_count(self):
		result = super().get_queryset().filter(Q(employmentstatus='Active') | Q(employmentstatus='Leave of Absence') | Q(employmentstatus='Future Start')).values('sex').annotate(count=Count('sex'))
		genderList = list(result)
		gender_dicts = [{dict['sex']: dict['count']} for dict in genderList]
		gender_counts = {k: v for d in gender_dicts for k, v in d.items()}
		return gender_counts

class StaffRaceCountManager(models.Manager):
	def race_count(self):
		result = super().get_queryset().filter(Q(employmentstatus='Active') | Q(employmentstatus='Leave of Absence') | Q(employmentstatus='Future Start')).values('racedesc').annotate(count=Count('racedesc'))
		raceList = list(result)
		race_dicts = [{dict['racedesc']: dict['count']} for dict in raceList]
		race_counts = {k: v for d in race_dicts for k, v in d.items()}
		return race_counts

class StaffMaritalStatusCountManager(models.Manager):
	def marital_count(self):
		result = super().get_queryset().filter(Q(employmentstatus='Active') | Q(employmentstatus='Leave of Absence') | Q(employmentstatus='Future Start')).values('maritaldesc').annotate(count=Count('maritaldesc'))
		maritalList = list(result)
		marital_dicts = [{dict['maritaldesc']: dict['count']} for dict in maritalList]
		marital_counts = {k: v for d in marital_dicts for k, v in d.items()}
		return marital_counts

class StaffRaceByDeptCountManager(models.Manager):
	def filter_count(self):
		defaults = {'American Indian or Alaska Native':0,'Asian':0,'Black or African American':0,'Hispanic':0,'Two or more races':0,'White':0}	
		result = super().get_queryset().filter(Q(employmentstatus='Active') | Q(employmentstatus='Leave of Absence') | Q(employmentstatus='Future Start')).values('department', 'racedesc').annotate(count=Count('racedesc')).distinct()
		output = defaultdict(dict)
		for dept in result:
			output[dept['department']][dept['racedesc']] = dept['count']
		raceDict = dict(output)
		for key in defaults.keys():
			for r in raceDict:
				raceDict[r].setdefault(key, defaults[key])			
		return raceDict

class StaffMaritalStatByDeptCountManager(models.Manager):
    def filter_count(self):
        defaults = {'Divorced':0,'Married':0,'Separated':0,'Single':0,'Widowed':0}
        result = super().get_queryset().filter(Q(employmentstatus='Active') | Q(employmentstatus='Leave of Absence') | Q(employmentstatus='Future Start')).values('department', 'maritaldesc').annotate(count=Count('maritaldesc')).distinct()
        output = defaultdict(dict)
        for dept in result:
            output[dept['department']][dept['maritaldesc']] = dept['count']
        statsDict = dict(output)
        for key in defaults.keys():
            for s in statsDict:
                statsDict[s].setdefault(key, defaults[key])			
        return statsDict

class StaffLocationByDeptCountManager(models.Manager):
    def locale_count(self):
        result = super().get_queryset().filter(Q(employmentstatus='Active') | Q(employmentstatus='Leave of Absence') | Q(employmentstatus='Future Start')).values('department', 'state').annotate(count=Count('state')).distinct()
        output = defaultdict(dict)
        for dept in result:
            output[dept['department']][dept['state']] = dept['count']
        localesDict = dict(output)	
        s = []
        for k,v in localesDict.items():
            states = list(v.keys())
            s.append(states)
        output = flatten(s)
        statesList = list(set(output))
        statesList.sort()
        
        return localesDict,statesList

class StaffAgeCountManager(models.Manager):
	def age_count(self):
		result = super().get_queryset().filter(Q(employmentstatus='Active') | Q(employmentstatus='Leave of Absence') | Q(employmentstatus='Future Start')).values('age').annotate(count=Count('age'))
		ageList = list(result)
		age_dicts = [{dict['age']: dict['count']} for dict in ageList]
		age_counts = {k: v for d in age_dicts for k, v in d.items()}
		sortedAgeCounts = dict(sorted(age_counts.items(), key = lambda x:x[0]))
		return sortedAgeCounts

class EmployeeListByWorkSiteManager(models.Manager):
    def emp_list(self, siteID):
        info = super().get_queryset().filter(Q(Q(employmentstatus='Active') | Q(employmentstatus='Leave of Absence') | Q(employmentstatus='Future Start')) & Q(worksiteid=siteID)).values('employeenumber','firstname','lastname','worksiteid','department','position','employmentstatus')
        return list(info)

class EmployeeZipCodeGroupsListManager(models.Manager):
    def filter_list(self):
        result = super().get_queryset().filter(Q(employmentstatus='Active') | Q(employmentstatus='Leave of Absence') | Q(employmentstatus='Future Start')).exclude(Q(worksiteid=2) | Q(worksiteid=3)).values('firstname','lastname','department','position','zip')
        dicts_list = list(result)
        allzips = [d['zip'] for d in dicts_list]
        zipCode_list = list(dict.fromkeys(allzips))
        [d.update({"zip": (str(d["zip"])).zfill(5)}) for d in dicts_list]        
        return zipCode_list, dicts_list

class ReasonForTerminationCountManager(models.Manager):
    def rft_count(self):
        result = super().get_queryset().exclude(reasonforterm__startswith='Not applicable').values('reasonforterm').annotate(count=Count('reasonforterm')).distinct()
        rftList = list(result)
        rft_dicts = [{dict['reasonforterm']: dict['count']} for dict in rftList]
        rft_counts = {k: v for d in rft_dicts for k, v in d.items()}
        rft_counts =  {k.capitalize(): v for k, v in rft_counts.items()}
        return rft_counts

class ReasonForTerminationByRaceCountManager(models.Manager):
    def rftRace_count(self):
        defaults = {'American Indian or Alaska Native':0,'Asian':0,'Black or African American':0,'Hispanic':0,'Two or more races':0,'White':0}
        result = super().get_queryset().exclude(reasonforterm__startswith='Not applicable').values('reasonforterm','racedesc').annotate(count=Count('reasonforterm')).distinct()
        output = defaultdict(dict)
        for r in result:
            output[r['reasonforterm']][r['racedesc']] = r['count']
        raceDict = dict(output)
        raceDict = {k.capitalize(): v for k, v in raceDict.items()}
        for key in defaults.keys():
            for s in raceDict:
                raceDict[s].setdefault(key, defaults[key])	
        return raceDict

class ReasonForTerminationByGenderCountManager(models.Manager):
    def rftGender_count(self):
        defaults = {'Male': 0, 'Female': 0}
        result = super().get_queryset().exclude(reasonforterm__startswith='Not applicable').values('reasonforterm', 'sex').annotate(count=Count('reasonforterm')).distinct()
        output = defaultdict(dict)
        for r in result:
            output[r['reasonforterm']][r['sex']] = r['count']
        sexDict = dict(output)
        sexDict = {k.capitalize(): v for k, v in sexDict.items()}
        for key in defaults.keys():
            for s in sexDict:
                sexDict[s].setdefault(key, defaults[key])	
        return sexDict

class PerformanceScoreCountManager(models.Manager):
    def perf_scores(self):
        result = super().get_queryset().filter(Q(employmentstatus='Active') | Q(employmentstatus='Leave of Absence') | Q(employmentstatus='Future Start')).values('performancescore').annotate(count=Count('performancescore'))
        perfScoreList = list(result)
        perfScore_dicts = [{dict['performancescore']: dict['count']} for dict in perfScoreList]
        perfScore_counts = {k: v for d in perfScore_dicts for k, v in d.items()}
        return perfScore_counts

class PerfScoreByDeptCountManager(models.Manager):
    def perf_scores(self):
        defaults = {'Not applicable - too early to review':0, 'Exceptional':0, '90-day meets':0, 'Fully Meets':0, 'Exceeds':0, 'PIP':0, 'Needs Improvement':0}		
        result = super().get_queryset().filter(Q(employmentstatus='Active') | Q(employmentstatus='Leave of Absence') | Q(employmentstatus='Future Start')).values('department', 'performancescore').annotate(count=Count('performancescore')).distinct()
        output = defaultdict(dict)
        for dept in result:
            output[dept['department']][dept['performancescore']] = dept['count']
        scoreDict = dict(output)
        for key in defaults.keys():
            for s in scoreDict:
                scoreDict[s].setdefault(key, defaults[key])
        return scoreDict

class EngageSurveyResultsByDeptManager(models.Manager):
    def dept_results(self):	
        result = super().get_queryset().filter(Q(employmentstatus='Active') | Q(employmentstatus='Leave of Absence') | Q(employmentstatus='Future Start')).exclude(Q(department='Executive Office')).values('department','engagementsurvey').order_by('department')
        resultList = list(result)
        temp = defaultdict(list)
        for item in resultList:
            temp[item['department']].append(item['engagementsurvey'])            
        output = [{'department':k, 'surveyresults':v} for k,v in temp.items()]        
        dept_lists = [{d['department']: d['surveyresults']} for d in output]
        for dept in dept_lists:	
            for val in dept.values():
                for i, e in enumerate(val):
                    val[i] = float(e)
        final_list = {k: v for d in dept_lists for k, v in d.items()}
        return final_list

class EmpSatSurveyResultsByDeptManager(models.Manager):
    def dept_results(self):	
        result = super().get_queryset().filter(Q(employmentstatus='Active') | Q(employmentstatus='Leave of Absence') | Q(employmentstatus='Future Start')).exclude(Q(department='Executive Office')).values('department','empsatisfaction').order_by('department')
        resultList = list(result)
        temp = defaultdict(list)
        for item in resultList:
            temp[item['department']].append(item['empsatisfaction'])            
        output = [{'department':k, 'surveyresults':v} for k,v in temp.items()]        
        dept_lists = [{d['department']: d['surveyresults']} for d in output]
        for dept in dept_lists:	
            for val in dept.values():
                for i, e in enumerate(val):
                    val[i] = float(e)
        final_list = {k: v for d in dept_lists for k, v in d.items()}
        return final_list

class HourlyPayDistribByDeptManager(models.Manager):
    def pay_distrib(self):	
        result = super().get_queryset().filter(Q(employmentstatus='Active') | Q(employmentstatus='Leave of Absence') | Q(employmentstatus='Future Start')).exclude(Q(department='Executive Office')).values('department','payrate').order_by('department')
        resultList = list(result)
        temp = defaultdict(list)
        for item in resultList:
            temp[item['department']].append(item['payrate'])            
        output = [{'department':k, 'pay':v} for k,v in temp.items()]        
        dept_lists = [{d['department']: d['pay']} for d in output]
        for dept in dept_lists:	
            for val in dept.values():
                for i, e in enumerate(val):
                    val[i] = float(e)
        final_list = {k: v for d in dept_lists for k, v in d.items()}
        return final_list

class HourlyPayDistribByGenderManager(models.Manager):
    def pay_distrib(self):	
        result = super().get_queryset().filter(Q(employmentstatus='Active') | Q(employmentstatus='Leave of Absence') | Q(employmentstatus='Future Start')).exclude(Q(department='Executive Office')).values('sex','payrate').order_by('sex')
        resultList = list(result)
        temp = defaultdict(list)
        for item in resultList:
            temp[item['sex']].append(item['payrate'])            
        output = [{'sex':k, 'pay':v} for k,v in temp.items()]        
        sex_lists = [{d['sex']: d['pay']} for d in output]
        for sex in sex_lists:	
            for val in sex.values():
                for i, e in enumerate(val):
                    val[i] = float(e)
        final_list = {k: v for d in sex_lists for k, v in d.items()}
        return final_list

class HourlyPayDistribByRaceManager(models.Manager):
    def pay_distrib(self):	
        result = super().get_queryset().filter(Q(employmentstatus='Active') | Q(employmentstatus='Leave of Absence') | Q(employmentstatus='Future Start')).exclude(Q(department='Executive Office')).values('racedesc','payrate').order_by('racedesc')
        resultList = list(result)
        temp = defaultdict(list)
        for item in resultList:
            temp[item['racedesc']].append(item['payrate'])            
        output = [{'racedesc':k, 'pay':v} for k,v in temp.items()]        
        race_lists = [{d['racedesc']: d['pay']} for d in output]
        for race in race_lists:	
            for val in race.values():
                for i, e in enumerate(val):
                    val[i] = float(e)
        final_list = {k: v for d in race_lists for k, v in d.items()}
        return final_list

class PreHireEmploymentSourceCountManager(models.Manager):
    def sources(self):
        result = super().get_queryset().filter(Q(employmentstatus='Active') | Q(employmentstatus='Leave of Absence') | Q(employmentstatus='Future Start')).values('employeesource').annotate(count=Count('employeesource'))
        sourceList = list(result)
        source_dicts = [{dict['employeesource']: dict['count']} for dict in sourceList]
        totalCounts = {k: v for d in source_dicts for k, v in d.items()}
        return totalCounts

class EmployeeData(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)
    lastname = models.TextField(db_column='LastName', blank=True, null=True)
    firstname = models.TextField(db_column='FirstName', blank=True, null=True)
    employeenumber = models.IntegerField(db_column='EmployeeNumber', blank=True, null=True)
    worksiteid = models.IntegerField(db_column='WorkSiteID', blank=True, null=True)
    marriedid = models.IntegerField(db_column='MarriedID', blank=True, null=True)
    maritalstatusid = models.IntegerField(db_column='MaritalStatusID', blank=True, null=True)
    genderid = models.IntegerField(db_column='GenderID', blank=True, null=True)
    empstatusid = models.IntegerField(db_column='EmpStatusID', blank=True, null=True)
    deptid = models.IntegerField(db_column='DeptID', blank=True, null=True)
    perfscoreid = models.IntegerField(db_column='PerfScoreID', blank=True, null=True)
    age = models.IntegerField(db_column='Age', blank=True, null=True)
    payrate = models.DecimalField(db_column='PayRate', max_digits=4, decimal_places=2, blank=True, null=True)
    state = models.TextField(db_column='State', blank=True, null=True)
    zip = models.IntegerField(db_column='Zip', blank=True, null=True)
    dob = models.DateTimeField(db_column='DOB', blank=True, null=True)
    sex = models.TextField(db_column='Sex', blank=True, null=True)
    maritaldesc = models.TextField(db_column='MaritalDesc', blank=True, null=True)
    citizendesc = models.TextField(db_column='CitizenDesc', blank=True, null=True)
    hispanic_latino = models.TextField(db_column='Hispanic_Latino', blank=True, null=True)
    racedesc = models.TextField(db_column='RaceDesc', blank=True, null=True)
    hiredate = models.DateTimeField(db_column='HireDate', blank=True, null=True)
    terminationdate = models.TextField(db_column='TerminationDate', blank=True, null=True)
    reasonforterm = models.TextField(db_column='ReasonForTerm', blank=True, null=True)
    employmentstatus = models.TextField(db_column='EmploymentStatus', blank=True, null=True)
    department = models.TextField(db_column='Department', blank=True, null=True)
    position = models.TextField(db_column='Position', blank=True, null=True)
    managername = models.TextField(db_column='ManagerName', blank=True, null=True)
    employeesource = models.TextField(db_column='EmployeeSource', blank=True, null=True)
    performancescore = models.TextField(db_column='PerformanceScore', blank=True, null=True)
    empsatisfaction = models.IntegerField(db_column='EmpSatisfaction', blank=True, null=True)
    engagementsurvey = models.DecimalField(db_column='EngagementSurvey', max_digits=4, decimal_places=2, blank=True, null=True)

    objects = models.Manager()
    empStatusCount = EmployeeStatusCountManager()
    staffDeptCount = StaffTotalsByDeptManager()
    staffGenderCount = StaffGenderCountManager()
    staffRaceCount = StaffRaceCountManager()
    staffMaritalStatCount = StaffMaritalStatusCountManager()
    staffRaceByDeptCount = StaffRaceByDeptCountManager()
    staffMaritalStatByDeptCount = StaffMaritalStatByDeptCountManager()
    staffLocationByDeptCount = StaffLocationByDeptCountManager()
    staffAgeCount = StaffAgeCountManager()
    empListByWorkSite = EmployeeListByWorkSiteManager()
    empZipCodeList = EmployeeZipCodeGroupsListManager()
    rftCount = ReasonForTerminationCountManager()
    rftCountByRace = ReasonForTerminationByRaceCountManager()
    rftCountByGender = ReasonForTerminationByGenderCountManager()
    perfScoreCount = PerformanceScoreCountManager()
    perfScoreByDeptCount = PerfScoreByDeptCountManager()
    engageSurveyResultsByDept = EngageSurveyResultsByDeptManager()
    empSatSurveyResultsByDept = EmpSatSurveyResultsByDeptManager()
    hourlyPayDistribByDept = HourlyPayDistribByDeptManager()
    hourlyPayDistribByGender = HourlyPayDistribByGenderManager()
    hourlyPayDistribByRace = HourlyPayDistribByRaceManager()
    preHireEmpSourceCount = PreHireEmploymentSourceCountManager()
    
    def __str__(self):
        return self.id

    class Meta:
        managed = False
        app_label = 'departments'
        db_table = 'Employee_Data'





"""
************************
* CASE MANAGEMENT DATA *
************************
"""
class UserCaseCountManager(models.Manager):
    def filter_count(self, userID, startDate, endDate):
        return super().get_queryset().filter(Q(caseowner=userID) & Q(datereceived__range=(startDate, endDate))).exclude(casestatus='Closed').count()

class UserOldCasesCountManager(models.Manager):
    def filter_count(self, userID, status, startDate, endDate):
        return super().get_queryset().filter(Q(caseowner=userID) & Q(casestatus=status) & Q(datereceived__range=(startDate, endDate))).count()

class TeamCaseCountManager(models.Manager):
    def filter_count(self, team, startDate, endDate):
        return super().get_queryset().filter(Q(casetype=team) & Q(datereceived__range=(startDate, endDate))).exclude(casestatus='Closed').count()

class TeamYTDCaseCountManager(models.Manager):
    def filter_count(self, team, startDate, endDate):
        return super().get_queryset().filter(Q(casetype=team) & Q(datereceived__range=(startDate, endDate))).count()
		
class TeamTierCaseCountManager(models.Manager):
    def filter_count(self, team, status, startDate, endDate):
        return super().get_queryset().filter(Q(casetype=team) & Q(casestatus=status) & Q(datereceived__range=(startDate, endDate))).count()

class TeamCurrentAvgCaseCloseNumPerMonthManager(models.Manager):
    def avg_count(self, team, startDate, endDate):
        results = super().get_queryset().filter(Q(casetype=team) & Q(datereceived__range=(startDate, endDate))).values_list('datereceived__month').annotate(avg_days=Avg(F('dateclosed__date') - F('datereceived__date')))
        resList = list(results)
        convertedList = [(calendar.month_abbr[num], avg.days) for num, avg in resList]
        months = list(month_abbr)
        finalList = sorted(convertedList, key = lambda i: months.index(i[0]))
        months = [i[0] for i in finalList]
        averages = [i[1] for i in finalList]
        return dict(zip(months, averages)) 

class TeamOpenCaseListManager(models.Manager):
    def case_list(self, team, startDate, endDate):
        result = super().get_queryset().filter(Q(casetype=team) & Q(datereceived__range=(startDate, endDate))).exclude(casestatus='Closed').values('caseid','tierlevel','caseowner','datereceived')
        resultList = list(result)
        [d.update({"caseowner":(HrCasesData.get_caseowner_name(d["caseowner"]))}) for d in resultList]
        finalList = [dict(list(i.items()) + [("OO_SLA", HrCasesData.is_out_of_SLA(i["tierlevel"],i["datereceived"]))]) for i in resultList]
        return finalList
        		
class TeamSatisfactionScoresManager(models.Manager):
	def score_count(self, team, startDate, endDate):
		result = super().get_queryset().filter(Q(casetype=team) & Q(casestatus='Closed') & Q(datereceived__range=(startDate, endDate))).values('satisfactionscore').annotate(count=Count('satisfactionscore'))
		scoresList = list(result)
		score_dicts = [{dict['satisfactionscore']: dict['count']} for dict in scoresList]
		scores = {k: v for d in score_dicts for k, v in d.items()}
		return scores

class TeamScoreCountByRequestorManager(models.Manager):
    def requestor_count(self, team, scoreType, startDate, endDate):
        result = super().get_queryset().filter(Q(casetype=team) & Q(satisfactionscore=scoreType) & Q(casestatus='Closed') & Q(datereceived__range=(startDate, endDate))).values('requestortype').annotate(count=Count('requestortype'))
        requestorList = list(result)
        requestor_dicts = [{dict['requestortype']: dict['count']} for dict in requestorList]
        info = {k: v for d in requestor_dicts for k, v in d.items()}
        return info

class TeamCaseRequestorTypeCountManager(models.Manager):
    def type_count(self, team, startDate, endDate):
        result = super().get_queryset().filter(Q(casetype=team) & Q(casestatus='Closed') & Q(datereceived__range=(startDate, endDate))).values('requestortype').annotate(count=Count('requestortype'))
        typesList = list(result)
        type_dicts = [{dict['requestortype']: dict['count']} for dict in typesList]
        types = {k: v for d in type_dicts for k, v in d.items()}
        return types

class TeamCasePriorityLevelCountManager(models.Manager):
    def level_count(self, team, startDate, endDate):
        result = super().get_queryset().filter(Q(casetype=team) & Q(casestatus='Closed') & Q(datereceived__range=(startDate, endDate))).values('priority').annotate(count=Count('priority'))
        levelsList = list(result)
        level_dicts = [{dict['priority']: dict['count']} for dict in levelsList]
        levels = {k: v for d in level_dicts for k, v in d.items()}
        return levels
        
class AllHRCaseCountManager(models.Manager):
    def filter_count(self, startDate, endDate):
        return super().get_queryset().exclude(casestatus = 'Closed').filter(datereceived__range=(startDate, endDate)).count()
		
class AllTeamsYTDCaseCountManager(models.Manager):
    def filter_count(self, startDate, endDate):
        return super().get_queryset().filter(Q(datereceived__range=(startDate, endDate))).values('casetype').annotate(count=Count('casetype')).distinct()

class AllTeamsCaseCountManager(models.Manager):
    def filter_count(self, startDate, endDate):
        return super().get_queryset().filter(Q(datereceived__range=(startDate, endDate))).exclude(casestatus='Closed').values('casetype').annotate(count=Count('casetype')).distinct()
		
class AllTeamsTierCaseCountManager(models.Manager):
    def filter_count(self, status, startDate, endDate):
        return super().get_queryset().filter(Q(casestatus=status) & Q(datereceived__range=(startDate, endDate))).values('casetype').annotate(count=Count('casetype')).distinct()
		
class AllTeamsSatisfactionScoresManager(models.Manager):
    def score_count(self, startDate, endDate):
        defaults = {'0 - Unknown':0,'1 - Unsatisfied':0,'2 - Satisfied':0,'3 - Highly satisfied':0}
        result = super().get_queryset().filter(Q(casestatus='Closed') & Q(datereceived__range=(startDate, endDate))).values('casetype', 'satisfactionscore').annotate(count=Count('satisfactionscore')).distinct()
        output = defaultdict(dict)
        for team in result:
            output[team['casetype']][team['satisfactionscore']] = team['count']
        scoresDict = dict(output)
        for key in defaults.keys():
            for s in scoresDict:
                scoresDict[s].setdefault(key, defaults[key])
        return scoresDict
		
class HrCasesData(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)
    caseid = models.TextField(db_column='CaseID', blank=True, null=True)
    requestorid = models.IntegerField(db_column='RequestorID', blank=True, null=True)
    requestortype = models.TextField(db_column='RequestorType', blank=True, null=True)
    caseowner = models.TextField(db_column='CaseOwner', blank=True, null=True)
    casetype = models.TextField(db_column='CaseType', blank=True, null=True)
    casestatus = models.TextField(db_column='CaseStatus', blank=True, null=True)
    tierlevel = models.TextField(db_column='TierLevel', blank=True, null=True)
    priority = models.TextField(db_column='Priority', blank=True, null=True)
    datereceived = models.DateTimeField(db_column='DateReceived', blank=True, null=True)
    satisfactionscore = models.TextField(db_column='SatisfactionScore', blank=True, null=True)
    dateclosed = models.DateTimeField(db_column='DateClosed', blank=True, null=True)

    objects = models.Manager()
    userCasesTotal = UserCaseCountManager()
    userOldCasesTotal = UserOldCasesCountManager()
    teamCasesTotal = TeamCaseCountManager()
    teamYTDCasesTotal = TeamYTDCaseCountManager()
    teamTierCasesTotal = TeamTierCaseCountManager()
    teamScores = TeamSatisfactionScoresManager()
    allHRCasesTotal = AllHRCaseCountManager()
    allTeamsYTDCasesTotal = AllTeamsYTDCaseCountManager()
    allTeamsCasesTotal = AllTeamsCaseCountManager()	
    allTeamsTierCasesTotal = AllTeamsTierCaseCountManager()
    allTeamsScores = AllTeamsSatisfactionScoresManager()
    teamRequestTypeCaseTotals = TeamCaseRequestorTypeCountManager()
    teamPriorityLevelCaseTotals = TeamCasePriorityLevelCountManager()
    teamOpenCasesList = TeamOpenCaseListManager()
    teamCurrAvgCaseCloseNumByMonth = TeamCurrentAvgCaseCloseNumPerMonthManager()
    teamScoreCountByRequestor = TeamScoreCountByRequestorManager()

    def __str__(self):
        return self.id

    def get_percentage(old_count, total_count):
        return 100-round((old_count/total_count)*100)
        
    def get_caseowner_name(memberID):
        info = HRTeamUser.objects.get(userid__exact = memberID)
        name = f"{info.firstname} {info.lastname}"
        return name

    def is_out_of_SLA(tier, rcvdDate):
        newDT = rcvdDate.replace(tzinfo=pytz.utc)
        if tier == "Tier 1":
            max_SLA_date = (datetime.datetime.now() - datetime.timedelta(days=2)).replace(tzinfo=pytz.utc)    
            if max_SLA_date < newDT:
                return False
            return True
        else:
            max_SLA_date = (datetime.datetime.now() - datetime.timedelta(days=4)).replace(tzinfo=pytz.utc)
            if max_SLA_date < newDT:
                return False
            return True       

    class Meta:
        managed = False
        app_label = 'departments'
        db_table = 'HR_Cases_Data'





"""
********************
* RECRUITMENT DATA *
********************
"""
class Recruitment2019MonthlyCosts(models.Manager):
    def costs(self):
        result = super().get_queryset().values('employmentsource','january_2019','february_2019','march_2019','april_2019','may_2019','june_2019','july_2019','august_2019','september_2019','october_2019','november_2019','december_2019')
        resultList = list(result)        
        output = defaultdict(list)
        for source in resultList:
            for key, val in source.items():
                if key != 'employmentsource':
                    output[source['employmentsource']].append(val)                
        return dict(output)


class RecruitingCosts2019(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)
    employmentsource = models.TextField(db_column='EmploymentSource', blank=True, null=True)
    january_2019 = models.IntegerField(db_column='January_2019', blank=True, null=True)
    february_2019 = models.IntegerField(db_column='February_2019', blank=True, null=True)
    march_2019 = models.IntegerField(db_column='March_2019', blank=True, null=True)
    april_2019 = models.IntegerField(db_column='April_2019', blank=True, null=True)
    may_2019 = models.IntegerField(db_column='May_2019', blank=True, null=True)
    june_2019 = models.IntegerField(db_column='June_2019', blank=True, null=True)
    july_2019 = models.IntegerField(db_column='July_2019', blank=True, null=True)
    august_2019 = models.IntegerField(db_column='August_2019', blank=True, null=True)
    september_2019 = models.IntegerField(db_column='September_2019', blank=True, null=True)
    october_2019 = models.IntegerField(db_column='October_2019', blank=True, null=True)
    november_2019 = models.IntegerField(db_column='November_2019', blank=True, null=True)
    december_2019 = models.IntegerField(db_column='December_2019', blank=True, null=True)

    objects = models.Manager()
    recruit2019Costs = Recruitment2019MonthlyCosts()

    def __str__(self):
        return self.employmentsource
	
    class Meta:
        managed = False
        app_label = 'departments'
        db_table = 'Recruiting_Costs_2019'





"""
*********************
* COMPENSATION DATA *
*********************
"""
class HourlyPayByPositionManager(models.Manager):
    def pay_ranges(self):
        result = super().get_queryset().values('position','hourly_min','hourly_mid','hourly_max')
        resultList = list(result)
        output = defaultdict(list)
        for i in resultList:
            output[i['position']].append(i['hourly_min'])        
            output[i['position']].append(i['hourly_mid'])
            output[i['position']].append(i['hourly_max'])
        for key,val in output.items():	
            for i, e in enumerate(val):
                val[i] = float(e)
        return dict(output)

class SalaryByPositionManager(models.Manager):
    def pay_ranges(self):
        result = super().get_queryset().values('position','salary_min','salary_mid','salary_max')
        resultList = list(result)
        output = defaultdict(list)
        for i in resultList:
            output[i['position']].append(i['salary_min'])        
            output[i['position']].append(i['salary_mid'])
            output[i['position']].append(i['salary_max'])
        for key,val in output.items():	
            for i, e in enumerate(val):
                val[i] = int(e)
        return dict(output)

class SalaryGrid2020(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)
    position = models.TextField(db_column='Position', blank=True, null=True)
    salary_min = models.IntegerField(db_column='Salary_Min', blank=True, null=True)
    salary_mid = models.IntegerField(db_column='Salary_Mid', blank=True, null=True)
    salary_max = models.IntegerField(db_column='Salary_Max', blank=True, null=True)
    hourly_min = models.DecimalField(db_column='Hourly_Min', max_digits=4, decimal_places=2, blank=True, null=True)
    hourly_mid = models.DecimalField(db_column='Hourly_Mid', max_digits=4, decimal_places=2, blank=True, null=True)
    hourly_max = models.DecimalField(db_column='Hourly_Max', max_digits=4, decimal_places=2, blank=True, null=True)
    
    objects = models.Manager()
    hourlyPayByPosition = HourlyPayByPositionManager()
    salaryByPosition = SalaryByPositionManager()

    def __str__(self):
        return self.id
	
    class Meta:
        managed = False
        app_label = 'departments'
        db_table = 'Salary_Grid_2020'





"""
***************************
* WORK SITE LOCATION DATA *
***************************
"""
class AllWorkSitesByLocationManager(models.Manager):
    def sites_info(self):
        info = super().get_queryset().exclude(sitename__startswith='Remote').values()
        dicts_list = list(info)
        [d.update({"zipcode": (str(d["zipcode"])).zfill(5)}) for d in dicts_list]
        return dicts_list

class AllWorkSitesByIDManager(models.Manager):
    def sites_info(self):
        info = super().get_queryset().values()        
        dicts_list = list(info)
        [d.update({"zipcode": (str(d["zipcode"])).zfill(5)}) for d in dicts_list]
        return dicts_list

class WorkSiteLocations(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)
    worksiteid = models.IntegerField(db_column='WorkSiteID', blank=True, null=True)
    sitename = models.TextField(db_column='SiteName', blank=True, null=True)
    address = models.TextField(db_column='Address', blank=True, null=True)
    city = models.TextField(db_column='City', blank=True, null=True)
    state = models.TextField(db_column='State', blank=True, null=True)
    zipcode = models.IntegerField(db_column='ZipCode', blank=True, null=True)
    mainphone = models.TextField(db_column='MainPhone', blank=True, null=True)
    image = models.TextField(db_column='Image', blank=True, null=True)

    objects = models.Manager()
    workSitesByLocationList = AllWorkSitesByLocationManager()
    workSitesByIDList = AllWorkSitesByIDManager()

    def __str__(self):
        return self.id
	
    class Meta:
        managed = False
        app_label = 'departments'
        db_table = 'Work_Site_Locations'
