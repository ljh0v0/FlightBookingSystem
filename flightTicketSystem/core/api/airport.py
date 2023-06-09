from django.contrib import auth
from django.contrib.auth.models import User
import core.models.airline
from django.shortcuts import render, HttpResponse, redirect

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

from core.models.permissions import (AIRLINE_CREATE, AIRLINE_VIEW, AIRLINE_CHANGE, CITY_VIEW,
                                     CITY_CHANGE, CITY_CREATE, AIRPORT_CHANGE, AIRPORT_CREATE,
                                     AIRPORT_VIEW)

'''

'''


@response_wrapper
@require_GET
def get_airport_info(request: HttpResponse):
    """
    :param request: GET
    :return:
        {
      "count": 2,
      "airports": [{
                      "airport_id": "1",
                      "airport_name": "长水国际机场",
                      "city": "昆明",
                      "start_time": "2012-06-28(日期格式可以自行规定)",
                      "location": "云南省昆明市官渡区长水村"
                  },
                  {
                      "airport_id": "2",
                      "airport_name": "大兴国际机场",
                      "city": "北京",
                      "start_time": "2019-09-15",
                      "location": "中国北京市大兴区/河北省廊坊市"
                  },
              ]
    }
    """
    airport_list = Airport.objects.all()
    count = 0
    airports = []

    city_str = request.GET.get('city_name')  # 南昌
    airport_str = request.GET.get('airport_name')  # 长水国际机场

    for ap in airport_list:
        if city_str is not None and ap.cityId.name != city_str:
            continue

        if airport_str is not None and ap.name != airport_str:
            continue

        count += 1
        city = ap.cityId
        city_name = city.name
        list_temp = {
            "airport_id": ap.airId,
            "airport_name": ap.name,
            "city": city_name,
            "start_time": ap.attTime,
            "location": ap.address
        }
        airports.append(list_temp)
    data = {
        "count": count,
        "airports": airports
    }
    return success_api_response(data)


@response_wrapper
@require_GET
def get_airport_detail_info(request: HttpResponse, airport_id: str):
    """
    :param airport_id: str
    :param request: GET
    :return:
        {
              {
                  "airport_id": "2",
                  "airport_name": "大兴国际机场",
                  "city": "北京",
                  "start_time": "2019-09-15",
                  "location": "中国北京市大兴区/河北省廊坊市"
              }
    }
    """

    airport_list = Airport.objects.filter(airId=airport_id)

    if airport_list.count() == 0:
        return failed_api_response(ErrorCode.ITEM_NOT_FOUND, "airport not found")
    ap = airport_list.first()

    data = {
        "airport_id": ap.airId,
        "airport_name": ap.name,
        "city": ap.cityId.name,
        "start_time": ap.attTime,
        "location": ap.address
    }
    return success_api_response(data)


@response_wrapper
@require_POST
@jwt_auth(perms=[AIRPORT_CREATE])
def init_airport_info(request: HttpResponse):
    """
        :param request: POST
        :return:
        {
          "airport_id": "1",
          "airport_name": "长水国际机场",
          "city": "昆明",
          "start_time": "2012-06-28(日期格式可以自行规定)",
          "location": "云南省昆明市官渡区长水村"
        }
        """

    body: dict = parse_data(request)
    airId = body['airport_id']
    name = body['airport_name']
    city_name = body['city']
    attTime = body['start_time']
    address = body['location']

    city_list = City.objects.filter(name=city_name)
    print(city_list.count())
    if city_list.count() == 0:
        return failed_api_response(ErrorCode.ITEM_NOT_FOUND, "city " + city_name + " not found")

    city = city_list.first()

    airport_list = Airport.objects.filter(airId=airId, cityId=city)
    if airport_list.count() > 0:
        return failed_api_response(ErrorCode.ITEM_ALREADY_EXISTS, "airport " + name + " already exist.")

    city = Airport(airId=airId, cityId=city, name=name, attTime=attTime, address=address)
    city.save()

    return success_api_response({"msg": "succeed init airport " + airId})


@response_wrapper
@require_http_methods(['DELETE'])
@jwt_auth(perms=[AIRPORT_CHANGE])
def dlt_airport_info(request: HttpResponse, airport_id: str):
    """
        :param airport_id:
        :param request: delete
        :return:
        """
    airport_find = Airport.objects.filter(airId=airport_id)

    if airport_find.count() == 0:
        return failed_api_response(ErrorCode.ITEM_NOT_FOUND, "airport not found.")
    Airport.objects.filter(airId=airport_id).delete()
    data = {"msg": "succeed delete"}
    return success_api_response(data)


airport_url = wrapped_api({
    "get": get_airport_info,
    "post": init_airport_info,
})

airport_detail_url = wrapped_api({
    "delete": dlt_airport_info,
    "get": get_airport_detail_info
})
