import datetime
import copy
from django.conf import settings
from django.db import models
from collections import OrderedDict
from django.db.models import F, Q, Count, Value
from dateutil import parser
from django.utils import timezone
from django.utils.timezone import make_aware
from datetime import timedelta
from . models import EmployeeData, HrCasesData, ProductionStaff, RecruitingCosts2018, SalaryGrid2019, TimeToFill5Yrs, WorkSiteLocations
from accounts.models import HRTeamUser

from random import randint
from django.views.generic import TemplateView
from chartjs.views.lines import BaseLineChartView

class LineChartJSONView(BaseLineChartView):
    def get_labels(self):
        """Return 7 labels for the x-axis."""
        return ["January", "February", "March", "April", "May", "June", "July"]

    def get_providers(self):
        """Return names of datasets."""
        return ["Central", "Eastside", "Westside"]

    def get_data(self):
        """Return 3 datasets to plot."""
        return [[75, 44, 92, 11, 44, 95, 35],
                [41, 92, 18, 3, 73, 87, 92],
                [87, 21, 94, 3, 90, 13, 65]]

