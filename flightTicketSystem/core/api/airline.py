from django.contrib import auth
from django.contrib.auth.models import User
import core.models.airline
from django.shortcuts import render, HttpResponse, redirect

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
@require_GET
def get_airline_info(request: HttpResponse):
    """
    :param request: GET
    :return:
    {
      "count": 2,
      "airllines": [{
                "airline_ids": "11,18,24",
                "from": "保山",
                "from_longitude": "99.1729",
                "from_latitude": "25.05753",
                "to": "南昌",
                "to_longitude": "115.9000015258789",
                "to_latitude": "28.864999771118164",
                "height": 483
                },
                {
                "airline_ids": "32,41,53,60,68,77,81",
                "from": "烟台",
                "from_longitude": "121.37200164794922",
                "from_latitude": "37.40169906616211",
                "to": "沈阳",
                "to_longitude": "123.48300170898438",
                "to_latitude": "41.639801025390625",
                "height": 237
                }]
    }
    """
    # body: dict = parse_data(request)
    # print(body)
    # from_str = body['from']
    # to_str = body['to']
    # airport_str = body['airport_id']
    from_str = request.GET.get('from')
    to_str = request.GET.get('to')
    airport_str = request.GET.get('airport_id')

    airline_list = Airline.objects.all()
    count = 0
    airlines = []
    for al in airline_list:
        from_city = al.oriCity
        if from_str != None and from_city.name != from_str:
            continue

        to_city = al.destCity
        if to_str != None and to_city.name != to_str:
            continue

        if airport_str != None:
            airport = Airport.objects.filter(name=airport_str)
            if airport.count()==0:
                continue
            if airport.first().cityId.name != al.oriCity.name and airport.first().cityId.name != al.destCity.name:
                continue

        count += 1
        list_temp = {
            "airline_ids": al.id,
            "from": al.oriCity.name,
            "from_longitude": al.oriCity.longitude,
            "from_latitude": al.oriCity.latitude,
            "to": al.destCity.name,
            "to_longitude": al.destCity.longitude,
            "to_latitude": al.destCity.latitude,
            "height": al.height
        }
        airlines.append(list_temp)
    data = {
        "count": count,
        "airlines": airlines
    }
    return success_api_response(data)


@response_wrapper
@require_POST
@jwt_auth(perms=[AIRLINE_CREATE])
def init_airline_info(request: HttpResponse):
    """
        :param request: POST
        :return:
         {
            "airline_id" : airline_id
            "from_city" : city_name (string)
            "to_city" : city_name
            "height" : height
        }

        """
    body: dict = parse_data(request)
    ori_city_name = body['from']
    dst_city_name = body['to']
    airline_id = body['airline_ids']
    height = body['height']

    ori_city_list = City.objects.filter(name=ori_city_name)
    dst_city_list = City.objects.filter(name=dst_city_name)
    if ori_city_list.count() != 1:
        return failed_api_response(ErrorCode.ITEM_NOT_FOUND, "origin city name's is not available.")
    if dst_city_list.count() != 1:
        return failed_api_response(ErrorCode.ITEM_NOT_FOUND, "destination city's name is not available.")
    ori_city = ori_city_list.first()
    dst_city = dst_city_list.first()

    airline_find = Airline.objects.filter(id=airline_id)
    if airline_find.count() > 0:
        return failed_api_response(ErrorCode.ITEM_ALREADY_EXISTS, "airline " + airline_id + " already exist.")

    airline = Airline(id=airline_id, oriCity=ori_city, destCity=dst_city, height=height)
    airline.save()

    return success_api_response({"msg": "succeed init airline " + airline_id})


@response_wrapper
@require_GET
def get_airline_info_detail(request: HttpResponse, airline_id: str):
    """
    :param airline_id: str
    :param request: GET
    :return:
    {
            "airline_ids": "11,18,24",
            "from": "保山",
            "from_longitude": "99.1729",
            "from_latitude": "25.05753",
            "to": "南昌",
            "to_longitude": "115.9000015258789",
            "to_latitude": "28.864999771118164",
            "height": 483
    }
    """
    airline_list = Airline.objects.filter(id=airline_id)
    if airline_list.count() == 0:
        return failed_api_response(ErrorCode.ITEM_NOT_FOUND, "do not exist airline " + airline_id)
    al = airline_list.first()
    data = {
        "airline_ids": al.id,
        "from": al.oriCity.name,
        "from_longitude": al.oriCity.longitude,
        "from_latitude": al.oriCity.latitude,
        "to": al.destCity.name,
        "to_longitude": al.destCity.longitude,
        "to_latitude": al.destCity.latitude,
        "height": al.height
    }
    return success_api_response(data)


@response_wrapper
@require_http_methods(['PATCH'])
@jwt_auth(perms=[AIRLINE_CHANGE])
def recps_airline_info(request: HttpResponse, airline_id: str):
    """
        :param airline_id: str
        :param request: PATCH
               airline_id: int
        :return:
         {
            "from_city" : city_name (string)
            "to_city" : city_name
            "height" : height
        }

        """
    airline_find = Airline.objects.filter(id=airline_id)
    if airline_find.count() == 0:
        return failed_api_response(ErrorCode.ITEM_NOT_FOUND, "airline " + airline_id + " not found exist.")
    airline = airline_find.first()

    body: dict = parse_data(request)
    ori_city_name = body['from_city']
    dst_city_name = body['to_city']
    height = body['height']

    if ori_city_name is not None:
        print(ori_city_name)
        ori_city_list = City.objects.filter(name=ori_city_name)
        if ori_city_list.count() != 1:
            return failed_api_response(ErrorCode.ITEM_NOT_FOUND, "origin city name's is not available.")
        ori_city = ori_city_list.first()
        airline.oriCity = ori_city
        airline.save()

    if dst_city_name is not None:
        dst_city_list = City.objects.filter(name=dst_city_name)
        if dst_city_list.count() != 1:
            return failed_api_response(ErrorCode.ITEM_NOT_FOUND, "destination city's name is not available.")
        dst_city = dst_city_list.first()
        airline.destCity = dst_city
        airline.save()

    if height is not None:
        airline.height = height
        airline.save()
    data = {"msg": "succeed recomposed " + airline_id}
    return success_api_response(data)


@response_wrapper
@require_http_methods(['DELETE'])
@jwt_auth(perms=[AIRLINE_CHANGE])
def dlt_airline_info(request: HttpResponse, airline_id: str):
    """
        :param airline_id:
        :param request: delete
        :return:
        """
    airline_find = Airline.objects.filter(id=airline_id)
    if airline_find.count() == 0:
        return failed_api_response(ErrorCode.ITEM_NOT_FOUND, "airline " + airline_id + " not found exist.")
    Airline.objects.filter(id=airline_id).delete()
    data = {"msg": "succeed delete " + airline_id}
    return success_api_response(data)


airline_url = wrapped_api({
    "get": get_airline_info,
    "post": init_airline_info,
})

airline_detail_url = wrapped_api({
    "get": get_airline_info_detail,
    "delete": dlt_airline_info,
    "patch": recps_airline_info
})

airline_detail_url = wrapped_api({
    "get": get_airline_info_detail,
    "patch": recps_airline_info,
    "delete": dlt_airline_info
})

# def get_info_total(request):
#     city_count = City.objects.count()
#     airport_count = Airport.objects.count()
#     airline_count = Airline.objects.count()
#     flight_count = Flight.objects.count()
#     data = {
#         'city_count': city_count,
#         'airport_count': airport_count,
#         'airline_count': airline_count,
#         'flight_count': flight_count
#     }
#     return data


'''
航线信息：

* 航线编号
* 始发城市信息
* 目的城市信息
* 航班信息列表
  * 航班编号
  * 当前状态
  * 所属航空公司
  * 所用飞机
  * 预计起飞时间 
  * 起点站
  * 预计到达时间
  * 终点站
  * 余票数
  * 总票数
  '''

# def get_search_flight(request):
#     date = request.POST.get('date')
#     ori_city = request.POST.get('ori_city')
#     dst_city = request.POST.get('dst_city')
#     company = request.POST.get('company')
#
#     data = {}
#     al_list = Airline.objects.filter(data=date).filter(oriCity=ori_city).filter(destCity=dst_city)
#     for al in al_list:
#         fl_list = Flight.objects.filter(airline=al.id).filter(ownedCpn=company)
#         for fl in fl_list:
#             ticket_count = -1
#             ticket_free_count = ticket_count - Ticket.objestc.filter(flightId=fl.id)
#             data_temp = {
#                 'airline_id': al.id,
#                 'ori_city': al.oriCity,
#                 'dst_city': al.destCity,
#                 'flight_id': fl.id,
#                 'flight_status': fl.status,
#                 'company': fl.ownedCpn,
#                 'plane': fl.plane,
#                 'fly_time': fl.flyTime,
#                 'ori_sta': fl.riStat,
#                 'arv_time': fl.arvTime,
#                 'dst_sta': al.destStat,
#                 'ticket_count': ticket_count,
#                 'ticket_free_count': ticket_free_count
#             }
#             data['flight_id'] = data_temp
#     return data
#
#
# def get_airport_info(request):
#     airport_id = request.POST.get('airport_id')
#     ap = Airport.objects.get(airId=airport_id)
#     cy = City.objects.get(id=ap.cityId)
#     fl1 = Flight.objects.filter(oriCity=cy.id)
#     fl2 = Flight.objects.filter(destCity=cy.id)
#     fl_list = {}
#     for fl in fl1:
#         fl_temp = {
#             'flight_id': fl.id,
#             'ori_city': fl.oriCity,
#             'dst_city': fl.destCity,
#             'height': fl.height,
#             'date': -1,
#         }
#         fl_list['fl'] = fl_temp
#     for fl in fl2:
#         fl_temp = {
#             'flight_id': fl.id,
#             'ori_city': fl.oriCity,
#             'dst_city': fl.destCity,
#             'height': fl.height,
#             'date': -1,
#         }
#         fl_list['fl'] = fl_temp
#     on_time1 = Flight.objects.filter(oriCity=cy.id).filter(status='A').filter(onTime=True)
#     delay1 = Flight.objects.filter(oriCity=cy.id).filter(status='A').filter(onTime=False)
#     on_time2 = Flight.objects.filter(destCity=cy.id).filter(status='A').filter(onTime=True)
#     delay2 = Flight.objects.filter(destCity=cy.id).filter(status='A').filter(onTime=False)
#     on_time_rate = (on_time2 + on_time1) / (on_time1 + on_time2 + delay1 + delay2)
#     cnp_info = Company.objects.all()
#     cnp_list = {}
#     total = 0
#     for cnp_list in cnp_info:
#         break
