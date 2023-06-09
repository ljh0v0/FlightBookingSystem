from django.contrib import auth
from django.contrib.auth.models import User
import core.models.airline
from django.shortcuts import render, HttpResponse, redirect

from core.models.airport import Airport
from core.models.flight import Flight
from core.models.ticket import Ticket
from core.models.company import Company

from core.api.utils import (ErrorCode, failed_api_response, require_item_exist,
                            response_wrapper, success_api_response,
                            validate_args, wrapped_api, parse_data)
from django.views.decorators.http import require_GET, require_POST, require_http_methods
from core.api.auth import jwt_auth

from core.models.permissions import (AIRLINE_CREATE, AIRLINE_VIEW, AIRLINE_CHANGE, CITY_VIEW,
                                     CITY_CHANGE, CITY_CREATE, COMPANY_VIEW, COMPANY_CREATE,
                                     COMPANY_CHANGE)

'''

'''


@response_wrapper
@require_GET
def get_cpn_info(request: HttpResponse):
    """
    :param request: GET
    :return:
    {
  "count": 2,
  "companies": [{
              "acro_name": "CEA",
              "full_name": "东方航空",
              "icon": "如果有返回icon的url, 否则为null",
              "on_rate": "0.83"
            },
            {
              "acro_name": "BUAA",
              "full_name": "北航",
              "icon": "如果有返回icon的url, 否则为null",
              "on_rate": "0.17"
            }
          ]
}
    }
    """
    cpn_list = Company.objects.all()
    count = 0
    cpns = []
    for cp in cpn_list:
        count += 1
        list_temp = {
            "acro_name": cp.acroName,
            "full_name": cp.fullName,
            "icon": cp.icon,
            "on_rate": cp.onRate,
        }
        cpns.append(list_temp)
    data = {
        "count": count,
        "companies": cpns
    }
    return success_api_response(data)


@response_wrapper
@require_GET
def get_cpn_info_detail(request: HttpResponse, acro_name: str):
    """
    :param acro_name:
    :param request: GET
    :return:
    {
              "acro_name": "BUAA",
              "full_name": "北航",
              "icon": "如果有返回icon的url, 否则为null",
              "on_rate": "0.17"
    }
    """
    cpn_list = Company.objects.filter(acroName=acro_name)
    if cpn_list.count() == 0:
        return failed_api_response(ErrorCode.ITEM_NOT_FOUND, "do not exist airway " + acro_name)
    cp = cpn_list.first()
    data = {
        "acro_name": cp.acroName,
        "full_name": cp.fullName,
        "icon": cp.icon,
        "on_rate": cp.onRate,
    }
    return success_api_response(data)


@response_wrapper
@require_POST
@jwt_auth(perms=[COMPANY_CREATE])
def init_cpn_info(request: HttpResponse):
    """
        :param request: POST
        :return:
         {
            "acro_name": cp.acroName,
            "full_name": cp.fullName,
            "icon": cp.icon,
            "on_rate": cp.onRate,
        }

        """

    body: dict = parse_data(request)
    acroName = body['acro_name']
    fullName = body['full_name']
    icon = body['icon']
    onRate = body['on_rate']

    cpn_find = Company.objects.filter(acroName=acroName)
    if cpn_find.count() > 0:
        return failed_api_response(ErrorCode.ITEM_ALREADY_EXISTS, "airways " + acroName + " already exist.")

    cpn = Company(acroName=acroName, fullName=fullName, icon=icon, onRate=onRate)
    cpn.save()

    return success_api_response({"msg": "succeed init airway " + acroName})


@response_wrapper
@require_http_methods(['DELETE'])
@jwt_auth(perms=[COMPANY_CHANGE])
def dlt_city_info(request: HttpResponse, acro_name: str):
    """
        :param acro_name:
        :param request: delete
        :return:
        """
    cpn_find = Company.objects.filter(acroName=acro_name)
    if cpn_find.count() == 0:
        return failed_api_response(ErrorCode.ITEM_NOT_FOUND, "airway " + acro_name + " not found.")
    Company.objects.filter(acroName=acro_name).delete()
    return success_api_response({"msg": "succeed delete " + acro_name})


cpn_url = wrapped_api({
    "get": get_cpn_info,
    "post": init_cpn_info
})

cpn_detail_url = wrapped_api({
    "get": get_cpn_info_detail,
    "delete": dlt_city_info
})
