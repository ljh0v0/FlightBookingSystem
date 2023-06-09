from django.contrib import auth
import core.models.airline
from django.shortcuts import render, HttpResponse, redirect

from core.models.airport import Airport
from core.models.city import City
from core.models.flight import Flight
from core.models.person import Person

from core.api.utils import (ErrorCode, failed_api_response, require_item_exist,
                            response_wrapper, success_api_response,
                            validate_args, wrapped_api, parse_data)
from django.views.decorators.http import require_GET, require_POST, require_http_methods
from core.api.auth import jwt_auth, verify_jwt_token

from core.models.permissions import (AIRLINE_CREATE, AIRLINE_VIEW, AIRLINE_CHANGE, CITY_VIEW,
                                     CITY_CHANGE, CITY_CREATE, AIRPORT_CHANGE, AIRPORT_CREATE,
                                     AIRPORT_VIEW, PERSON_CREATE, PERSON_VIEW, PERSON_CHANGE)

'''

'''


@response_wrapper
@require_GET
def get_person_info(request: HttpResponse):
    """
    :param request: GET
    :return:
        {
        count:2
        userInfo:{
                    "id": "532502200006150012",
                    "sex": "女",
                    "birth": "2000-06-15",
                    "upor": "北京",
                    "name": "柳嘉禾",
                    "phone": "13988261194",
                }
    }
    """
    person_list = Person.objects.all()
    #print(person_list.count())
    count = 0
    people = []
    for ps in person_list:
        count += 1
        list_temp = {
            "id": ps.id,
            "sex": ps.sex,
            "birth": ps.birthday,
            "upor": ps.upor,
            "name": ps.name,
            "phone": ps.username,
            "password": ps.password
        }
        people.append(list_temp)
    data = {
        "count": count,
        "userInfo": people
    }
    return success_api_response(data)


@response_wrapper
@require_GET
def get_person_info_detail(request: HttpResponse):
    """
    :param user_id: int  phone number
    :param request: GET
    :return:
    {
        "id": "532502200006150012",
        "sex": "女",
        "birth": "2000-06-15",
        "upor": "北京",
        "name": "柳嘉禾",
        "phone": "13988261194",
    }
    """

    print(111)
    verify, msg, user_id = verify_jwt_token(request)
    if verify is False:
        print("!!!!!!!!!!!!!!")
        return failed_api_response(ErrorCode.PERSON_NOT_FOUND, msg)

    person_list = Person.objects.filter(username=user_id)
    if len(person_list) == 0:
        return failed_api_response(ErrorCode.ITEM_NOT_FOUND, "do not exist person " + str(user_id))
    ps = person_list.first()
    data = {
        "id": ps.id,
        "sex": ps.sex,
        "birth": ps.birthday,
        "upor": ps.upor,
        "name": ps.name,
        "phone": ps.username,
        "auth": ps.auth
    }
    return success_api_response(data)


@response_wrapper
@require_http_methods(['PATCH'])
def recps_person_info(request: HttpResponse, user_id: str):
    """
        :param user_id: int
        :param request: PATCH
        :return:
         {
           "id": "532502200006150012",
            "sex": "女",
            "birth": "2000-06-15",
            "upor": "北京",
            "name": "柳嘉禾",
            "phone": "13988261194" phone can't be change
        }

        """
    person_list = Person.objects.filter(username=user_id)
    if len(person_list) == 0:
        return failed_api_response(ErrorCode.ITEM_NOT_FOUND, "person " + user_id + " not found exist.")
    person = person_list[0]

    body: dict = parse_data(request)
    id = body['id']
    sex = body['sex']
    birth = body['birth']
    upor = body['upor']
    name = body['name']

    if sex != None:
        person.sex = sex
        person.save()

    if birth != None:
        person.birth = birth
        person.save()

    if upor != None:
        person.upor = upor
        person.save()

    if name != None:
        person.name = name
        person.save()

    if id != None:
        person.id = id
        person.save()


    return success_api_response({"msg": "succeed recomposed " + user_id})


@response_wrapper
@require_http_methods(['DELETE'])
@jwt_auth(perms=[PERSON_CHANGE])
def dlt_person_info(request: HttpResponse, user_id: str):
    """
        :param user_id:
        :param request: delete
        :return:
        """
    user_find = Person.objects.filter(username=user_id)
    if user_find.count() == 0:
        return failed_api_response(ErrorCode.ITEM_NOT_FOUND, "user not found.")
    Person.objects.filter(username=user_id).delete()
    return success_api_response({"msg":"succeed delete."})


person_url = wrapped_api({
    "get": get_person_info
})

person_detail_url = wrapped_api({

    "patch": recps_person_info,
    "delete": dlt_person_info
})

person_token_url = wrapped_api({
    "get": get_person_info_detail
})
