from django.contrib import auth
from django.contrib.auth.models import User
import core.models.airline
from django.shortcuts import render, HttpResponse, redirect

from core.models.company import Company
from core.models.plane import Plane

from core.api.utils import (ErrorCode, failed_api_response, require_item_exist,
                            response_wrapper, success_api_response,
                            validate_args, wrapped_api, parse_data)
from django.views.decorators.http import require_GET, require_POST, require_http_methods
from core.api.auth import jwt_auth

from core.models.permissions import (AIRLINE_CREATE, AIRLINE_VIEW, AIRLINE_CHANGE, CITY_VIEW,
                                     CITY_CHANGE, CITY_CREATE, PLANE_CREATE)

'''

'''


@response_wrapper
@require_GET
def get_plane_info(request: HttpResponse):
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
    plane_list = Plane.objects.all()
    for pl in plane_list:
        print(pl.pid)

    data = {
        "msg": "I am useless, why i am here?"
    }
    return success_api_response(data)


@response_wrapper
@require_POST
@jwt_auth(perms=[PLANE_CREATE])
def init_plane_info(request: HttpResponse):
    """
        :param request: POST
        :return:
         {
    "pid" = "1",
    "attTime" = "1",
    "mileage" = "1",
    "ownedCpn" = "BUAA",
    "type" = "播音747"
    "price" = "1",
    "voyCnt" = "1",
    "seatCnt" = "1"
        }

        """
    body: dict = parse_data(request)
    pid = body['pid']
    attTime = body['attTime']
    mileage = body['mileage']
    ownedCpn = body['ownedCpn']
    price = body['price']
    type = body['type']
    voyCnt = body['voyCnt']
    seatCnt = body['seatCnt']

    plane_find = Plane.objects.filter(pid=pid)
    if plane_find.count() > 0:
        return failed_api_response(ErrorCode.ITEM_ALREADY_EXISTS, "plane " + pid + " already exist.")

    cpn = Company.objects.filter(acroName=ownedCpn).first()
    plane = Plane(pid=pid, attTime=attTime, mileage=mileage, ownedCpn=cpn, price=price, voyCnt=voyCnt, seatCnt=seatCnt, type=type)
    plane.save()

    return success_api_response({"msg": "succeed init plane " + pid})


plane_url = wrapped_api({
    "GET": get_plane_info,
    "POST": init_plane_info,
})
