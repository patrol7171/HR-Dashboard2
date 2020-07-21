from accounts.models import HRTeamUser
from departments.models import EmployeeData, HrCasesData, RecruitingCosts2019, SalaryGrid2020, WorkSiteLocations

class HRDataRouter(object): 
    def db_for_read(self, model, **hints):
        if model in (HRTeamUser, EmployeeData, HrCasesData, RecruitingCosts2019, SalaryGrid2020, WorkSiteLocations):
            return 'hr_data'

    def db_for_write(self, model, **hints):
        return 'default'
    
    def allow_relation(self, obj1, obj2, **hints):
        return True
    
    def allow_migrate(self, db, app_label, model_name=None, **hints):
        return True