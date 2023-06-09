from django.contrib import auth
from django.contrib.auth.models import User
import core.models.airline
from django.shortcuts import render, HttpResponse, redirect

from core.models.airport import Airport
from core.models.city import City
from core.models.airline import Airline
from core.models.flight import Flight
from core.models.ticket import Ticket
from core.models.company import Company
from core.models.plane import Plane

from core.api.utils import (ErrorCode, failed_api_response, require_item_exist,
                            response_wrapper, success_api_response,
                            validate_args, wrapped_api, parse_data)
from django.views.decorators.http import require_GET, require_POST, require_http_methods
from core.api.auth import jwt_auth

from core.models.permissions import (AIRLINE_CREATE, AIRLINE_VIEW, AIRLINE_CHANGE, FLIGHT_VIEW,
                                     FLIGHT_CREATE, FLIGHT_CHANGE)

'''

'''


@response_wrapper
@require_GET
def get_flight_info(request: HttpResponse):
    """
    :param request: GET
    :return:
    {
  "count": 2,
  "flights": [{
                "flight_id": "东航MU5100",
                "current_status": "等待",
                "airport": "东方航空",
                "airplane": "空客330",
                "depart_time": "07:00",
                "from": "首都T2",
                "arrive_time": "09:12",
                "to": "上海虹桥",
                "all_tickets": "200",
                "left_tickets": "89",
                "date": 2020.1.1
            },
            {
                "flight_id": "南航CZ9308",
                "current_status": "等待",
                "airport": "南方航空",
                "airplane": "波音737",
                "depart_time": "07:00",
                "from": "长水机场",
                "arrive_time": "08:35",
                "to": "双流T2",
                "all_tickets": "200",
                "left_tickets": "112",
                "date": 2020.1.1
            }
          ]
}
    """

    # body: dict = parse_data(request)
    # from_str = body['from']
    # to_str = body['to']
    # date_str = body['date']
    # cpn_str = body['company']

    from_str = request.GET.get('from')
    to_str = request.GET.get('to')
    date_str = request.GET.get('date')
    cpn_str = request.GET.get('company')
    search_dict = dict()
    if from_str != None:
        search_dict['airline_id__oriCity_id__name'] = from_str
    if to_str != None:
        search_dict['airline_id__destCity_id__name'] = to_str
    if date_str != None:
        search_dict["flyDate"] = date_str
    if cpn_str != None:
        search_dict['ownedCpn_id__fullName'] = cpn_str
    flight_list = Flight.objects.filter(**search_dict)
    #flight_list = Flight.objects.all()
    #print(from_str)
    count = 0
    flights = []
    for fl in flight_list:
        #print(fl.fid)
        #from_city = fl.airline.oriCity
        #print(from_city.name)
        #print(from_str)
        #if from_str != None and from_city.name != from_str:
            #print(1)
        #    continue

        #to_city = fl.airline.destCity
        #if to_str != None and to_city.name != to_str:
            #print(2)
        #    continue

        #date = fl.flyDate
        #if date_str is not None and str(date) != date_str:
            #print(3)
        #    continue

        #cpn = fl.ownedCpn
        #if cpn_str != None and cpn.acroName != cpn_str:
            #print(4)
        #    continue

        count += 1
        list_temp = {
            "flight_id": fl.fid,
            "current_status": fl.status,
            "company": fl.ownedCpn.fullName,
            "airplane": fl.plane.type,
            "depart_time": fl.flyTime,
            "from": fl.oriStat.name,
            "arrive_time": fl.arvTime,
            "to": fl.destStat.name,
            "all_tickets": fl.plane.seatCnt,
            "left_c_tickets": fl.cAvaSeat,
            "left_e_tickets": fl.eAvaSeat,
            "date": fl.flyDate,
            "eprice": fl.eprice,
            "cprice": fl.cprice,
            "ontime": fl.onTime

        }
        flights.append(list_temp)
    data = {
        "count": count,
        "flights": flights
    }
    return success_api_response(data)


@response_wrapper
@require_POST
@jwt_auth(perms=[FLIGHT_CREATE])
def init_flight_info(request: HttpResponse):
    """
        :param request: POST
        :return:
         {
            "flight_id": "东航MU5100",
            "current_status": "等待",
            "company": "东方航空",
            "airplane": "pid",
            "depart_time": "07:00",
            "from": "首都T2",
            "arrive_time": "09:12",
            "to": "上海虹桥",
            "left_tickets": "89",

            "airline" : "所属航线",
            "on_time": "是否准时",

            "cprice": 100,
            "eprice": 200,
        }

        """
    body: dict = parse_data(request)
    flight_id = body['flight_id']
    status = body['current_status']
    ownedCpn = body['company']
    plane = body['airplane']
    flyTime = body['depart_time']
    oriStat = body['from']
    arvTime = body['arrive_time']
    destStat = body['to']
    cAvaSeat = body['left_c_tickets']
    eAvaSeat = body['left_e_tickets']
    airline = body['airline']
    onTime = body['on_time']
    flyDate = body['date']
    cprice = body['cprice']
    eprice = body['eprice']

    airline = Airline.objects.filter(id=airline).first()
    ownedCpn = Company.objects.filter(acroName=ownedCpn).first()
    oriStat = Airport.objects.filter(name=oriStat).first()
    destStat = Airport.objects.filter(name=destStat).first()
    plane = Plane.objects.filter(pid=plane).first()

    if Flight.objects.filter(fid=flight_id).count() != 0:
        return failed_api_response(ErrorCode.ITEM_ALREADY_EXISTS, "duplicate flight")
    flight = Flight(fid=flight_id, status=status, ownedCpn=ownedCpn, plane=plane, flyTime=flyTime, flyDate=flyDate,
                    oriStat=oriStat, arvTime=arvTime, destStat=destStat, cAvaSeat=cAvaSeat, eAvaSeat=eAvaSeat,
                    airline=airline,
                    onTime=onTime, eprice=eprice, cprice=cprice)
    flight.save()

    return success_api_response({"msg": "succeed init airline " + flight_id})


@response_wrapper
@require_GET
def get_flight_info_detail(request: HttpResponse, flight_id: str):
    """
    :param flight_id:
    :param request: GET

    :return:
    {
                "flght_id": "东航MU5100",
                "current_status": "等待",
                "company": "东方航空",
                "airplane": "空客330",
                "depart_time": "07:00",
                "from": "首都T2",
                "arrive_time": "09:12",
                "to": "上海虹桥",
                "all_tickets": "200",
                "left_c_tickets": "89",
                "left_e_tickets": "89",
                "ontime": True
            }
    """
    flight_list = Flight.objects.filter(fid=flight_id)
    if flight_list.count() == 0:
        return failed_api_response(ErrorCode.ITEM_NOT_FOUND, "do not exist flight " + flight_id)
    fl = flight_list.first()
    data = {
        "flght_id": fl.fid,
        "current_status": fl.status,
        "company": fl.ownedCpn.fullName,
        "airplane": fl.plane.type,
        "depart_time": fl.flyTime,
        "from": fl.oriStat.name,
        "arrive_time": fl.arvTime,
        "to": fl.destStat.name,
        "all_tickets": fl.plane.seatCnt,
        "left_c_tickets": fl.cAvaSeat,
        "left_e_tickets": fl.eAvaSeat,
        "eprice": fl.eprice,
        "cprice": fl.cprice,
        "ontime": fl.onTime
    }
    return success_api_response(data)


@response_wrapper
@require_http_methods(['PATCH'])
@jwt_auth(perms=[FLIGHT_CHANGE])
def recps_flight_info(request: HttpResponse, flight_id: str):
    """
        :param flight_id: str
        :param request: PATCH
        :return:
         {
            "current_status": "等待",
            "depart_time": "07:00",
            "arrive_time": "09:12",
            "ontime": True
        }

        """
    flight_find = Flight.objects.filter(fid=flight_id)
    if flight_find.count() == 0:
        return failed_api_response(ErrorCode.ITEM_NOT_FOUND, "flight " + flight_id + " not found exist.")
    flight = flight_find.first()

    #print(flight)
    body: dict = parse_data(request)
    #print("11111")
    #print(body)
    status = body['current_status']
    flyTime = body['depart_time']
    arvTime = body['arrive_time']
    cprice = body['cprice']
    eprice = body['eprice']
    ontime = body['ontime']

    if status is not None:
        flight.status = status
        flight.save()

    if flyTime is not None:
        flight.flyTime = flyTime
        flight.save()

    if arvTime is not None:
        flight.arvTime = arvTime
        flight.save()

    if cprice is not None:
        flight.cprice = cprice
        flight.save()

    if eprice is not None:
        flight.eprice = eprice
        flight.save()

    if ontime is not None:
        flight.onTime = ontime
        flight.save()

    return success_api_response({"msg": "succeed recomposed " + flight_id})


@response_wrapper
@require_http_methods(['DELETE'])
@jwt_auth(perms=[FLIGHT_CHANGE])
def dlt_flight_info(request: HttpResponse, flight_id: str):
    """
        :param flight_id: str
        :param request: delete
               airline_id: int
        :return:
        """
    flight_find = Flight.objects.filter(fid=flight_id)
    if flight_find.count() == 0:
        return failed_api_response(ErrorCode.ITEM_NOT_FOUND, "airline " + flight_id + " not found exist.")
    Flight.objects.filter(fid=flight_id).delete()
    return success_api_response({"msg": "succeed delete " + flight_id})


flight_url = wrapped_api({
    "get": get_flight_info,
    "post": init_flight_info
})

flight_detail_url = wrapped_api({
    "get": get_flight_info_detail,
    "patch": recps_flight_info,
    "delete": dlt_flight_info
})
