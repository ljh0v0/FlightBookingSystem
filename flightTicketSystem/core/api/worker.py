from django.contrib import auth
from django.contrib.auth.models import User
import core.models.airline
from django.shortcuts import render, HttpResponse, redirect

from core.models.airport import Airport
from core.models.city import City
from core.models.airline import Airline
from core.models.flight import Flight
from core.models.person import Person
from core.models.pilot import Pilot, PilotFlight
from core.models.steward import Steward
from core.models.ticket import Ticket
from core.models.company import Company
from core.models.plane import Plane

from core.api.utils import (ErrorCode, failed_api_response, require_item_exist,
                            response_wrapper, success_api_response,
                            validate_args, wrapped_api, parse_data)
from django.views.decorators.http import require_GET, require_POST, require_http_methods
from core.api.auth import jwt_auth

from core.models.permissions import (AIRLINE_CREATE, AIRLINE_VIEW, AIRLINE_CHANGE, FLIGHT_VIEW,
                                     FLIGHT_CREATE, FLIGHT_CHANGE, PILOT_CREATE)

'''

'''


@response_wrapper
@require_GET
def get_worker_info(request: HttpResponse):
    """
    :param request: GET
    :return:
    {
  "count": 2,
  "workers": [{
                "person_id": "1101032000000000000", # 电话号码
                "fly_time": "123",
                "company": "东方航空",
                "emp_date": "2020-12-12",
                "pos" : "机长"
            },
            {
                "person_id": "1101032000000000000",
                "fly_time": "123",
                "company": "东方航空",
                "emp_date": "2020-12-12",
                "pos" : "机长"
            }
          ]
}
    """

    pilot_list = Pilot.objects.all()
    steward_list = Steward.objects.all()

    count = 0
    workers = []
    for pl in pilot_list:
        count += 1
        list_temp = {
            "person_id": pl.pid.username,
            "name": pl.pid.name,
            "fly_time": pl.flyTime,
            "company": pl.ownedCpn.fullName,
            "emp_date": pl.empDate,
            "pos": pl.pos
        }
        workers.append(list_temp)

    for sw in steward_list:
        count += 1
        list_temp = {
            "person_id": sw.pid.username,
            "name": sw.pid.name,
            "fly_time": sw.servTime,
            "company": sw.ownedCpn.fullName,
            "emp_date": sw.empDate,
            "pos": sw.pos
        }
        workers.append(list_temp)

    data = {
        "count": count,
        "flights": workers
    }
    return success_api_response(data)


@response_wrapper
@require_POST
@jwt_auth(perms=[PILOT_CREATE])
def init_worker_info(request: HttpResponse):
    """
        :param request: POST
        :return:
         {
            "person_id": "1101032000000000000", # 电话号码
            "fly_time": "123",
            "company": "东方航空",
            "emp_date": "2020-12-12",
            "pos" : "机长",
            "type" : "pilot"
            #pilot; steward
        }

        """
    body: dict = parse_data(request)

    type = body['type']
    pid = body['person_id']
    flyTime = body['fly_time']
    ownedCpn = body['company']
    empDate = body['emp_date']
    pos = body['pos']

    ownedCpn = Company.objects.filter(acroName=ownedCpn).first()
    person = Person.objects.filter(username=pid).first()

    if type == 'pilot':
        if Pilot.objects.filter(pid=person).count() != 0:
            return failed_api_response(ErrorCode.ITEM_ALREADY_EXISTS, "duplicate pilot")
        pilot = Pilot(pid=person, flyTime=flyTime, ownedCpn=ownedCpn, empDate=empDate, pos=pos)
        pilot.save()
    elif type == 'steward':
        if Steward.objects.filter(pid=person).count() != 0:
            return failed_api_response(ErrorCode.ITEM_ALREADY_EXISTS, "duplicate steward")
        steward = Steward(pid=person, servTime=flyTime, ownedCpn=ownedCpn, empDate=empDate, pos=pos)
        steward.save()
    else:
        return failed_api_response(ErrorCode.ITEM_NOT_FOUND, "undefined type")
    return success_api_response({"msg": "succeed init worker."})


@response_wrapper
@require_GET
def get_relation_info_detail(request: HttpResponse):
    """
    :param flight_id:
    :param request: GET

    :return:
   {
  "count": 2,
  "workers": [{
                "person_id": "1101032000000000000", # 电话号码
                "fly_time": "123",
                "company": "东方航空",
                "emp_date": "2020-12-12",
                "pos" : "机长"
            },
            {
                "person_id": "1101032000000000000",
                "fly_time": "123",
                "company": "东方航空",
                "emp_date": "2020-12-12",
                "pos" : "机长"
            }
          ]
}
    """
    flight_str = request.GET.get('flight')

    pilot_list = Pilot.objects.all()
    steward_list = Steward.objects.all()

    count = 0
    workers = []
    for pl in pilot_list:
        flight_list = pl.flight.filter(fid=flight_str)
        if flight_list.count() == 0:
            continue
        count += 1
        list_temp = {
            "person_id": pl.pid.username,
            "name": pl.pid.name,
            "fly_time": pl.flyTime,
            "company": pl.ownedCpn.fullName,
            "emp_date": pl.empDate,
            "pos": pl.pos
        }
        workers.append(list_temp)

    for sw in steward_list:
        flight_list = sw.flight.filter(fid=flight_str)
        if flight_list.count() == 0:
            continue
        count += 1
        list_temp = {
            "person_id": sw.pid.username,
            "name": sw.pid.name,
            "fly_time": sw.servTime,
            "company": sw.ownedCpn.fullName,
            "emp_date": sw.empDate,
            "pos": sw.pos
        }
        workers.append(list_temp)

    data = {
        "count": count,
        "flights": workers
    }
    return success_api_response(data)

@response_wrapper
@require_POST
@jwt_auth(perms=[FLIGHT_CHANGE])
def init_relation_info(request: HttpResponse):
    """
        {
        "type" : "pilot", #pilot and steward
        "person_id": "123456", #phone
        "flight": "MU123_2" #flight_id
        }
    """
    body: dict = parse_data(request)

    type = body['type']
    pid = body['person_id']
    fid = body['flight']

    flight = Flight.objects.filter(fid=fid).first()
    person = Person.objects.filter(username=pid).first()

    if type == 'pilot':
        pilot = Pilot.objects.filter(pid=person).first()
        pilot.flight.add(flight)
        pilot.save()
    elif type == 'steward':
        steward = Steward.objects.filter(pid=person).first()
        steward.flight.add(flight)
        steward.save()
    else:
        return failed_api_response(ErrorCode.ITEM_NOT_FOUND, "undefined type")
    return success_api_response({"msg": "succeed init relation."})


worker_url = wrapped_api({
    "get": get_worker_info,
    "post": init_worker_info
})

relation_url = wrapped_api({
    "get": get_relation_info_detail,
    "post": init_relation_info
})
