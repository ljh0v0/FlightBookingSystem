from django.contrib import auth
from django.contrib.auth.models import User
import core.models.airline
from django.shortcuts import render, HttpResponse, redirect
import datetime

from core.models.airline import Airline
from core.models.airport import Airport
from core.models.city import City
from core.models.flight import Flight
from core.models.ticket import Ticket
from core.models.company import Company

from core.api.utils import (ErrorCode, failed_api_response, require_item_exist,
                            response_wrapper, success_api_response,
                            validate_args, wrapped_api, parse_data)
from django.views.decorators.http import require_GET, require_POST, require_http_methods
from core.api.auth import jwt_auth

from core.models.permissions import (AIRLINE_CREATE, AIRLINE_VIEW, AIRLINE_CHANGE)

'''

'''


@response_wrapper
def get_cpn_total(request):
    
    temp = {}
    
    body: dict = parse_data(request)
    airId = body['airport_id']
    flight = Flight.objects.filter(oriStat_id__airId=airId)
    cpn = Company.objects.all()

    count = 0
    for c in cpn:
        #print(c.fullName)
        temp[c.fullName] = 0
        count += 1
    for fl in flight:
        temp[fl.ownedCpn.fullName] += 1
    companies = []
    for key, value in temp.items():
        #print(key)
        #print(value)
        companies.append({"value": value, "name": key})
    data = {
        "count": count,
        "companies": companies
    }
    return success_api_response(data)


@response_wrapper
def get_on_time(request):
    

    body: dict = parse_data(request)
    airId = body['airport_id']
    flight = Flight.objects.filter(oriStat_id__airId=airId, status="已到达")
    count = 0
    ontime = 0
    for fl in flight:
        """if fl.oriStat.airId == airId and fl.status == "已到达":
            count += 1
            if fl.onTime:
                ontime += 1"""
        count += 1
        if fl.onTime:
            ontime += 1

    if count != 0:
        rate = ontime/count
    else:
        rate = 0
    data = {
        "on_time_rate": rate
    }
    return success_api_response(data)


@response_wrapper
def get_flow(request):
    

    body: dict = parse_data(request)
    airId = body['airport_id']
    
    this_date = datetime.datetime.strptime('2020-12-24', '%Y-%m-%d').date()
    flight = Flight.objects.filter(oriStat_id__airId=airId, flyDate=this_date)
    time = []
    for i in range(0, 24):
        time.append(0)
    for fl in flight:
        
        """if fl.oriStat.airId != airId:
            continue

        if fl.flyDate == this_date:
            hour = fl.flyTime.hour
            time[hour] += 1"""
        hour = fl.flyTime.hour
        time[hour] += 1

    data = {
        "flight_flow": time
    }
    return success_api_response(data)
