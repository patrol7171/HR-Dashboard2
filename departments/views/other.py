import requests
import datetime
import copy
import collections
import us
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import generic, View
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from dateutil import parser
from django.utils import timezone
from django.utils.timezone import make_aware
from collections import defaultdict
from datetime import timedelta
from departments.forms import SiteDropDownForm
from departments.models import EmployeeData, WorkSiteLocations
from geocodio import GeocodioClient

GEOCODIO_API_KEY = settings.GEOCODIO_API_KEY
MAPBOX_API_KEY = settings.MAPBOX_API_KEY





@login_required
def demographics(request):
    status = EmployeeData.empStatusCount.status_count()
    deptCount = EmployeeData.staffDeptCount.dept_count()
    gender = EmployeeData.staffGenderCount.gender_count()
    race = EmployeeData.staffRaceCount.race_count()
    marital = EmployeeData.staffMaritalStatCount.marital_count()
    raceByDeptValues = EmployeeData.staffRaceByDeptCount.filter_count()
    maritalStatByDeptValues = EmployeeData.staffMaritalStatByDeptCount.filter_count()
    age = EmployeeData.staffAgeCount.age_count()
    localeCount = EmployeeData.staffLocationByDeptCount.locale_count()
    
    statusValues = [status['Voluntarily Terminated'], status['Terminated for Cause'], status['Active'], status['Future Start'], status['Leave of Absence']]
    deptCountValues = [deptCount['Executive Office'], deptCount['Admin Offices'], deptCount['IT - Information Systems'], deptCount['Production'], deptCount['Sales'], deptCount['Software Engineering']]
    genderValues = [gender['Male'],gender['Female']]
    raceValues = [race['American Indian or Alaska Native'],race['Asian'],race['Black or African American'],race['Hispanic'],race['Two or more races'],race['White']]
    maritalStatValues = [marital['Divorced'],marital['Married'],marital['Separated'],marital['Single'],marital['Widowed']]
    ageCountValues = [list(age.keys()),list(age.values())]
    localesByDeptInfo = [localeCount[0],localeCount[1]]

    context = {"demographics_page":"active","statusValues":statusValues,"deptCountValues":deptCountValues,"genderValues":genderValues,"raceValues":raceValues,
    "maritalStatValues":maritalStatValues,"raceByDeptValues":raceByDeptValues,"maritalStatByDeptValues":maritalStatByDeptValues, "ageCountValues":ageCountValues,
    "localesByDeptInfo":localesByDeptInfo}

    return render(request, 'departments/demographics.html', context)
	


@login_required
def locater(request, tabnum):
    if tabnum == 1:
        activeTab = "emplist_tab"
    elif tabnum == 2:
        activeTab = "worksites_tab"       
    else:
        activeTab = "emphomelist_tab"

    form1 = SiteDropDownForm(request.POST or None)
    sitesList = WorkSiteLocations.workSitesByLocationList.sites_info()
    map_js = []
    response = ""

    if ('locations_info' in request.session) and ('state_list' in request.session):
        locations_info = request.session['locations_info']
        state_list = request.session['state_list']

    else:
        loc_list = []
        state_list = [] 
        locations_info = []        
        client = GeocodioClient(GEOCODIO_API_KEY)
        infoLists = EmployeeData.empZipCodeList.filter_list()
        zipList = infoLists[0]
        empByZipList = infoLists[1]

        try:
            response = client.geocode(zipList)
            for resp_dict in response:
                for dk1, dv1 in resp_dict.items():
                    if dk1 == 'results': 
                        d = {}
                        result_dicts = dv1[0]
                        addr_comp = result_dicts.get('address_components')
                        d['state'] = addr_comp.get('state')
                        d['zip'] = addr_comp.get('zip')
                        d['lat'] = result_dicts.get('location').get('lat')
                        d['long'] = result_dicts.get('location').get('lng')
                        loc_list.append(d)

            d1 = {d['zip']:d for d in loc_list}
            final_loc_list = [dict(d, **d1.get(d['zip'], {})) for d in empByZipList]           
            
            temp = defaultdict(list) 
            for item in final_loc_list:
                temp[item['state']].append(item)
            loc_groups = dict(temp)
            
            for dk2, dv2 in loc_groups.items():
                state_name = str(us.states.lookup(dk2))
                state_list.append(state_name)
                locations_info.append({state_name:dv2})
 
            request.session['state_list'] = state_list
            request.session['locations_info'] = locations_info
            
        except Exception as e:
            response = "error"
            print(response)
    
    if response == "error":
        error_html = "var error_html = '<br><br><br><br><h3>An error occurred, and the map is unavailable at this time</h3><lead>Please check back later.</lead>';" 
        error_js = "$('#leaflet-maps').append(error_html);"
        map_js.append(error_html)    
        map_js.append(error_js)
    else:
        map_js = get_map_js(locations_info)       
    
    if request.method == 'POST':
        site_ID = request.POST.get('site')
        request.session['site_ID'] = site_ID
    else:       
        if 'site_ID' in request.session:
            site_ID = request.session['site_ID']
            form1.fields['site'].initial = site_ID
        else:
            site_ID = 1
            
    employee_list = EmployeeData.empListByWorkSite.emp_list(site_ID)        
    page = request.GET.get('page', 1)
    paginator = Paginator(employee_list, 10)
    try:
        empList = paginator.page(page)
    except PageNotAnInteger:
        empList = paginator.page(1)
    except EmptyPage:
        empList = paginator.page(paginator.num_pages)   
    
    maps_js_code = ' '.join(map_js)
    context = {"locater_page":"active","jobaid_menu":"active",activeTab:"active","sitesList":sitesList,"empList":empList,'form1':form1,
    "state_list":state_list,"maps_js_code":maps_js_code}   
    
    return render(request, 'departments/locater.html', context)



def get_map_js(info):
    mapHREF = "https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}?access_token={accessToken}"
    attrib = "&copy; <a href='https://www.openstreetmap.org/copyright' target='_blank'>OpenStreetMap</a> contributors"
    mapboxid = "mapbox/streets-v11"
    key = MAPBOX_API_KEY
    resize_code = []
    map_code = []
    
    for index, val in enumerate(info, start=1):
        mapName = 'mymap'+str(index)
        mapid = 'mapid'+str(index)
        map_str = ''
        ctr_lat = ''
        ctr_long = ''
        all_markers = []
        for data in val.values():
            for d in data:
                if d == data[0]:
                    first_dict = d
                    ctr_lat = first_dict.get('lat')
                    ctr_long = first_dict.get('long')
                lat = d.get('lat')
                long = d.get('long')                
                dept = d.get('department')
                deptDict = {'dept': dept}
                icon = get_icon_color(**deptDict)
                pos = d.get('position')
                fname = d.get('firstname')
                lname = d.get('lastname')
                marker_cluster_str = f'L.marker([{lat},{long}],{icon}).bindPopup("{fname} {lname} <br/>{pos}")'
                all_markers.append(marker_cluster_str)

        all_markers_str = ','.join(all_markers)
        map_str = f'var {mapName} = L.map("{mapid}",{{center:[{ctr_lat}, {ctr_long}], maxZoom: 18}}).setView([{ctr_lat}, {ctr_long}], 9);  L.tileLayer("{mapHREF}", {{attribution:"{attrib}", id:"{mapboxid}", tileSize:512, zoomOffset:-1, accessToken:"{key}"}}).addTo({mapName});' 
        resize_func = f'$("#employeehomelist1").on("shown.bs.tab", function(event) {{ {mapName}.invalidateSize(); }});'
        cluster_str = f'var {mapName}Markers = L.markerClusterGroup(); var {mapName}MarkerList = [{all_markers_str}]; for (var i=0; i<{mapName}MarkerList.length; i++) {{ {mapName}Markers.addLayer({mapName}MarkerList[i]); }}; {mapName}.addLayer({mapName}Markers);'
        final_js_string = map_str + cluster_str        
        map_code.append(final_js_string)
        resize_code.append(resize_func)
    
    all_resize_funcs = ' '.join(resize_code)
    map_code.append(all_resize_funcs)
    
    return map_code



def get_icon_color(dept):
    icon_colors = {'Executive Office':'{icon: greenIcon}', 'Admin Offices':'{icon: goldIcon}', 'IT - Information Systems':'{icon: violetIcon}', 'Software Engineering':'{icon: redIcon}', 'Production':'{icon: orangeIcon}', 'Sales':'{icon: blueIcon}'}
    color = icon_colors.get(dept)
    
    return color