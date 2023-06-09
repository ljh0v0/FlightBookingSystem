from django.contrib import auth
from django.contrib.auth.models import User
import core.models.airline
from django.shortcuts import render, HttpResponse, redirect

from core.models.airport import Airport
from core.models.deparGate import DeparGate

from core.api.utils import (ErrorCode, failed_api_response, require_item_exist,
                            response_wrapper, success_api_response,
                            validate_args, wrapped_api, parse_data)
from django.views.decorators.http import require_GET, require_POST, require_http_methods
from core.api.auth import jwt_auth

from core.models.permissions import (AIRLINE_CREATE, AIRLINE_VIEW, AIRLINE_CHANGE, CITY_VIEW,
                                     CITY_CHANGE, CITY_CREATE, PLANE_CREATE, DEPAR_GATE_CREATE)

'''

'''


@response_wrapper
@require_GET
def get_gate_info(request: HttpResponse):
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
    gate_list = DeparGate.objects.all()
    for gate in gate_list:
        print(gate.depId)

    data = {
        "msg": "I am useless, why i am here?"
    }
    return success_api_response(data)


@response_wrapper
@require_POST
@jwt_auth(perms=[DEPAR_GATE_CREATE])
def init_gate_info(request: HttpResponse):
    """
        :param request: POST
        :return:
         {
    "depId" : "A",
    "airId" : "长水国际机场"

        }

        """
    body: dict = parse_data(request)
    depId = body['depId']
    airId = body['airId']

    airport = Airport.objects.filter(name=airId).first()

    gate = DeparGate(depId=depId, airId=airport)
    gate.save()

    return success_api_response({"msg": "succeed init gate " + depId})


gate_url = wrapped_api({
    "GET": get_gate_info,
    "POST": init_gate_info,
})
