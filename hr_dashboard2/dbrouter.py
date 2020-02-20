from accounts.models import HRTeamUser
from departments.models import EmployeeData, HrCasesData, ProductionStaff, RecruitingCosts2018, SalaryGrid2019, TimeToFill5Yrs, WorkSiteLocations

class HRDataRouter(object): 
    def db_for_read(self, model, **hints):
        if model in (HRTeamUser, EmployeeData, HrCasesData, ProductionStaff, RecruitingCosts2018, SalaryGrid2019, TimeToFill5Yrs, WorkSiteLocations):
            return 'hr_data'

    def db_for_write(self, model, **hints):
        return 'default'
    
    def allow_relation(self, obj1, obj2, **hints):
        return True
    
    def allow_migrate(self, db, app_label, model_name=None, **hints):
        return True