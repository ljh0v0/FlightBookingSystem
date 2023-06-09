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
                                     CITY_CHANGE, CITY_CREATE)

'''

'''


@response_wrapper
@require_GET
def get_city_info(request: HttpResponse):
    """
    :param request: GET
    :return:
    {
      {
  "count": 2,
  "cities": [{
              "id": "BS",
              "name": "保山",
              "longitude": "99.1729",
              "latitude": "25.05753",
              "province": "云南"
            },
            {
              "id": "NC",
              "name": "南昌",
              "longitude": "115.9000015258789",
              "latitude": "28.864999771118164",
              "province": "江西"
            }
          ]
}
    }
    """
    city_list = City.objects.all()
    count = 0
    cities = []
    for ct in city_list:
        count += 1
        list_temp = {
            "ids": ct.id,
            "name": ct.name,
            "longitude": ct.longitude,
            "latitude": ct.latitude,
            "province": ct.province
        }
        cities.append(list_temp)
    data = {
        "count": count,
        "cities": cities
    }
    return success_api_response(data)


@response_wrapper
@require_POST
@jwt_auth(perms=[CITY_CREATE])
def init_city_info(request: HttpResponse):
    """
        :param request: POST
        :return:
         {
            "id": "NC",
            "name": "南昌",
            "longitude": "115.9000015258789",
            "latitude": "28.864999771118164",
            "province": "江西"
        }

        """
    body: dict = parse_data(request)
    city_id = body['id']
    name = body['name']
    longitude = body['longitude']
    latitude = body['latitude']
    province = body['province']

    city_find = City.objects.filter(id=city_id)
    if city_find.count() > 0:
        return failed_api_response(ErrorCode.ITEM_ALREADY_EXISTS, "city " + city_id + " already exist.")

    city = City(id=city_id, name=name, longitude=longitude, latitude=latitude, province=province)
    city.save()

    return success_api_response({"msg": "succeed init city " + city_id})


@response_wrapper
@require_http_methods(['DELETE'])
@jwt_auth(perms=[CITY_CHANGE])
def dlt_city_info(request: HttpResponse, city_id: str):
    """
        :param city_id:
        :param request: delete
               airline_id: int
        :return:
        """
    city_find = City.objects.filter(id=city_id)
    if city_find.count()== 0:
        return failed_api_response(ErrorCode.ITEM_NOT_FOUND, "city " + city_id + " not found exist.")
    City.objects.filter(id=city_id).delete()
    data = {
        "msg" :"succeed delete " + city_id
    }
    return success_api_response(data)


city_url = wrapped_api({
    "GET": get_city_info,
    "POST": init_city_info,
})

city_detail_url = wrapped_api({
    "DELETE": dlt_city_info
})
