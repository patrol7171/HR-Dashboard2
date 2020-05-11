from django.conf import settings
from django.db import models
from django.contrib.auth.models import Group
from django.db.models import F, Q, Count, Value
from collections import OrderedDict, defaultdict






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

class StaffAgeCountManager(models.Manager):
	def age_count(self):
		result = super().get_queryset().filter(Q(employmentstatus='Active') | Q(employmentstatus='Leave of Absence') | Q(employmentstatus='Future Start')).values('age').annotate(count=Count('age'))
		ageList = list(result)
		age_dicts = [{dict['age']: dict['count']} for dict in ageList]
		age_counts = {k: v for d in age_dicts for k, v in d.items()}
		sortedAgeCounts = dict(sorted(age_counts.items(), key = lambda x:x[0]))
		return sortedAgeCounts

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

	objects = models.Manager()
	empStatusCount = EmployeeStatusCountManager()
	staffDeptCount = StaffTotalsByDeptManager()
	staffGenderCount = StaffGenderCountManager()
	staffRaceCount = StaffRaceCountManager()
	staffMaritalStatCount = StaffMaritalStatusCountManager()
	staffRaceByDeptCount = StaffRaceByDeptCountManager()
	staffMaritalStatByDeptCount = StaffMaritalStatByDeptCountManager()
	staffAgeCount = StaffAgeCountManager()

	def __str__(self):
		return self.id

	class Meta:
		managed = False
		app_label = 'departments'
		db_table = 'Employee_Data'




class UserCaseCountManager(models.Manager):
    def filter_count(self, userID, startDate, endDate):
        return super().get_queryset().filter(Q(caseowner=userID) & Q(datereceived__range=(startDate, endDate))).exclude(casestatus = 'Closed').count()

class UserOldCasesCountManager(models.Manager):
    def filter_count(self, userID, status, startDate, endDate):
        return super().get_queryset().filter(Q(caseowner=userID) & Q(casestatus=status) & Q(datereceived__range=(startDate, endDate))).count()

class TeamCaseCountManager(models.Manager):
    def filter_count(self, team, startDate, endDate):
        return super().get_queryset().filter(Q(casetype=team) & Q(datereceived__range=(startDate, endDate))).exclude(casestatus = 'Closed').count()

class TeamYTDCaseCountManager(models.Manager):
    def filter_count(self, team, startDate, endDate):
        return super().get_queryset().filter(Q(casetype=team) & Q(datereceived__range=(startDate, endDate))).count()
		
class TeamTierCaseCountManager(models.Manager):
    def filter_count(self, team, status, startDate, endDate):
        return super().get_queryset().filter(Q(casetype=team) & Q(casestatus=status) & Q(datereceived__range=(startDate, endDate))).count()
		
class TeamSatisfactionScoresManager(models.Manager):
	def score_count(self, team, startDate, endDate):
		result = super().get_queryset().filter(Q(casetype=team) & Q(casestatus='Closed') & Q(datereceived__range=(startDate, endDate))).values('satisfactionscore').annotate(count=Count('satisfactionscore'))
		scoresList = list(result)
		score_dicts = [{dict['satisfactionscore']: dict['count']} for dict in scoresList]
		scores = {k: v for d in score_dicts for k, v in d.items()}
		return scores

class AllHRCaseCountManager(models.Manager):
    def filter_count(self, startDate, endDate):
        return super().get_queryset().exclude(casestatus = 'Closed').filter(datereceived__range=(startDate, endDate)).count()
		
class AllTeamsYTDCaseCountManager(models.Manager):
    def filter_count(self, startDate, endDate):
        return super().get_queryset().filter(Q(datereceived__range=(startDate, endDate))).values('casetype').annotate(count=Count('casetype')).distinct()

class AllTeamsCaseCountManager(models.Manager):
    def filter_count(self, startDate, endDate):
        return super().get_queryset().filter(Q(datereceived__range=(startDate, endDate))).exclude(casestatus = 'Closed').values('casetype').annotate(count=Count('casetype')).distinct()
		
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

	def __str__(self):
		return self.id

	def get_percentage(old_count, total_count):
		return 100-round((old_count/total_count)*100)

	class Meta:
		managed = False
		app_label = 'departments'
		db_table = 'HR_Cases_Data'



class ProductionStaff(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)
    lastname = models.TextField(db_column='LastName', blank=True, null=True)
    firstname = models.TextField(db_column='FirstName', blank=True, null=True)
    racedesc = models.TextField(db_column='RaceDesc', blank=True, null=True)
    hiredate = models.DateTimeField(db_column='HireDate', blank=True, null=True)
    termdate = models.TextField(db_column='TermDate', blank=True, null=True)
    reasonforterm = models.TextField(db_column='ReasonForTerm', blank=True, null=True)
    employmentstatus = models.TextField(db_column='EmploymentStatus', blank=True, null=True)
    department = models.TextField(db_column='Department', blank=True, null=True)
    position = models.TextField(db_column='Position', blank=True, null=True)
    pay = models.TextField(db_column='Pay', blank=True, null=True)
    managername = models.TextField(db_column='ManagerName', blank=True, null=True)
    performancescore = models.TextField(db_column='PerformanceScore', blank=True, null=True)
    abutmentsperhourwk1 = models.IntegerField(db_column='AbutmentsPerHourWk1', blank=True, null=True)
    abutmentsperhourwk2 = models.IntegerField(db_column='AbutmentsPerHourWk2', blank=True, null=True)
    dailyerrorrate = models.IntegerField(db_column='DailyErrorRate', blank=True, null=True)
    complaints_90days = models.IntegerField(db_column='Complaints_90Days', blank=True, null=True)
	
    def __str__(self):
        return self.id
	
    class Meta:
        managed = False
        app_label = 'departments'
        db_table = 'Production_Staff'



class RecruitingCosts2018(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)
    employmentsource = models.TextField(db_column='EmploymentSource', blank=True, null=True)
    january_2018 = models.IntegerField(db_column='January_2018', blank=True, null=True)
    february_2018 = models.IntegerField(db_column='February_2018', blank=True, null=True)
    march_2018 = models.IntegerField(db_column='March_2018', blank=True, null=True)
    april_2018 = models.IntegerField(db_column='April_2018', blank=True, null=True)
    may_2018 = models.IntegerField(db_column='May_2018', blank=True, null=True)
    june_2018 = models.IntegerField(db_column='June_2018', blank=True, null=True)
    july_2018 = models.IntegerField(db_column='July_2018', blank=True, null=True)
    august_2018 = models.IntegerField(db_column='August_2018', blank=True, null=True)
    september_2018 = models.IntegerField(db_column='September_2018', blank=True, null=True)
    october_2018 = models.IntegerField(db_column='October_2018', blank=True, null=True)
    november_2018 = models.IntegerField(db_column='November_2018', blank=True, null=True)
    december_2018 = models.IntegerField(db_column='December_2018', blank=True, null=True)

    def __str__(self):
        return self.employmentsource
	
    class Meta:
        managed = False
        app_label = 'departments'
        db_table = 'Recruiting_Costs_2018'



class SalaryGrid2019(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)
    position = models.TextField(db_column='Position', blank=True, null=True)
    salary_min = models.IntegerField(db_column='Salary_Min', blank=True, null=True)
    salary_mid = models.IntegerField(db_column='Salary_Mid', blank=True, null=True)
    salary_max = models.IntegerField(db_column='Salary_Max', blank=True, null=True)
    hourly_min = models.DecimalField(db_column='Hourly_Min', max_digits=4, decimal_places=2, blank=True, null=True)
    hourly_mid = models.DecimalField(db_column='Hourly_Mid', max_digits=4, decimal_places=2, blank=True, null=True)
    hourly_max = models.DecimalField(db_column='Hourly_Max', max_digits=4, decimal_places=2, blank=True, null=True)

    def __str__(self):
        return self.position
	
    class Meta:
        managed = False
        app_label = 'departments'
        db_table = 'Salary_Grid_2019'



class TimeToFill5Yrs(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)
    fiscalyear = models.IntegerField(db_column='FiscalYear', blank=True, null=True)
    quarter = models.TextField(db_column='Quarter', blank=True, null=True)
    department = models.TextField(db_column='Department', blank=True, null=True)
    processstartdate = models.DateTimeField(db_column='ProcessStartDate', blank=True, null=True)
    recruitmentdate = models.DateTimeField(db_column='RecruitmentDate', blank=True, null=True)
    position = models.TextField(db_column='Position', blank=True, null=True)
    employeesource = models.TextField(db_column='EmployeeSource', blank=True, null=True)
    totaldaysforrecruitmentcompletion = models.IntegerField(db_column='TotalDaysForRecruitmentCompletion', blank=True, null=True)
    positiontypegoal = models.IntegerField(db_column='PositionTypeGoal', blank=True, null=True)
    successfulrecruitment = models.IntegerField(db_column='SuccessfulRecruitment', blank=True, null=True)

    def __str__(self):
        return self.id
	
    class Meta:
        managed = False
        app_label = 'departments'
        db_table = 'Time_To_Fill_5yrs'



class WorkSiteLocations(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)
    siteid = models.IntegerField(db_column='SiteID', blank=True, null=True)
    sitename = models.TextField(db_column='SiteName', blank=True, null=True)
    address = models.TextField(db_column='Address', blank=True, null=True)
    city = models.TextField(db_column='City', blank=True, null=True)
    state = models.TextField(db_column='State', blank=True, null=True)
    zipcode = models.IntegerField(db_column='ZipCode', blank=True, null=True)
    mainphone = models.TextField(db_column='MainPhone', blank=True, null=True)

    def __str__(self):
        return self.sitename
	
    class Meta:
        managed = False
        app_label = 'departments'
        db_table = 'Work_Site_Locations'

