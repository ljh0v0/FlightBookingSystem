from django.contrib import auth
from django.contrib.auth.models import User
import core.models.airline
from django.shortcuts import render, HttpResponse, redirect

from core.models.airport import Airport
from core.models.city import City
from core.models.deparGate import DeparGate
from core.models.flight import Flight
from core.models.person import Person
from core.models.ticket import Ticket
from core.models.company import Company

from core.api.utils import (ErrorCode, failed_api_response, require_item_exist,
                            response_wrapper, success_api_response,
                            validate_args, wrapped_api, parse_data)
from django.views.decorators.http import require_GET, require_POST, require_http_methods
from core.api.auth import jwt_auth, verify_jwt_token

from core.models.permissions import (AIRLINE_CREATE, AIRLINE_CHANGE,
                                     CITY_CHANGE, CITY_CREATE, TICKET_CHANGE, TICKET_VIEW, TICKET_CREATE, FLIGHT_CHANGE)

'''

'''


@response_wrapper
@require_GET
@jwt_auth(perms=[TICKET_VIEW])
def get_ticket_info(request: HttpResponse):
    """
    :param request: GET
    :return:
        {
  "count": 2,
  "trip_reocrds": [
                    {
                        "flight_id":"东航MU5100",
                        "depart_time": "07:00",
                        "from": "首都T2",
                        arrive_time: "09:12",
                        to: "上海虹桥",
                        seat_id: "12A",
                        ticket_type: "经济舱",
                        gate: "10",
                        price: 620,
                        person_id: "532502200006150012",
                        sale_time: "2020-11-21",
                        phone: "13988261194",
                        detail: ""
                    },
                    {
                        flight_id:"东航MU5100",
                        depart_time: "07:00",
                        from: "首都T2",
                        arrive_time: "09:12",
                        to: "上海虹桥",
                        seat_id: "12A",
                        ticket_type: "经济舱",
                        gate: "10",
                        price: 620,
                        person_id: "532502200006150012",
                        sale_time: "2020-11-21",
                        phone: "13988261194",
                        detail: ""
                    },
                ]
}
    """
    #ticket_list = Ticket.objects.all()
    verify, msg, user_id = verify_jwt_token(request)
    if verify is False:
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS, msg)

    search_dict = dict()
    if user_id != None:
        search_dict['passengerId_id__username'] = user_id
    ticket_list = Ticket.objects.filter(**search_dict)
    #print(user_id)
    """
        ('W', '等待'),
        ('C', '检票中'),
        ('L', '晚点'),
        ('F', '飞行中'),
        ('A', '已到达'),
        ('D', '失联')
    """
    count = 0
    tickets = []
    status = request.GET.get('status')
    for tk in ticket_list:
        if status != None:
            status = int(status)
            if ~status:
                if tk.flightId.status == '飞行中' or tk.flightId.status == '已到达' or tk.flightId.status == '失联':
                    continue
            if status:
                if tk.flightId.status == '等待' or tk.flightId.status == '检票中' or tk.flightId.status == '晚点':
                    continue

        #print(tk.passengerId.username)
        #print(user_id)
        #if user_id != None and tk.passengerId.username != user_id:
        #    continue
        count += 1
        #print(tk.gate)
        list_temp = {
            "flight_id": tk.flightId.fid,
            "depart_time": tk.flightId.flyTime,
            "from": tk.flightId.oriStat.name,
            "arrive_time": tk.flightId.arvTime,
            "to": tk.flightId.destStat.name,
            "status": tk.flightId.status,
            "seat_id": tk.seatId,
            "ticket_type": tk.type,
            "gate": tk.gate.depId,
            "price": tk.price,
            "person_id": tk.passengerId.username,
            "sale_time": tk.saleTime,
            "detail": tk.detail
        }
        tickets.append(list_temp)
    data = {
        "count": count,
        "airports": tickets
    }
    return success_api_response(data)


@response_wrapper
@require_POST
@jwt_auth(perms=[TICKET_CREATE])
def init_ticket_info(request: HttpResponse):
    """
        :param request: POST
        :return:
        {
            "flight_id": tk.flightId,
            "seat_id": tk.seatId,
            "ticket_type": tk.type,
            "gate": tk.gate,
            "price": tk.price,
            "detail": tk.detail
        }
        """
    body: dict = parse_data(request)
    flightId = body['flight_id']
    seatId = body['seat_id']
    gate = body['gate']
    type = body['ticket_type']
    price = body['price']
    saleTime = body['sale_time']
    detail = body['detail']

    verify, msg, user_id = verify_jwt_token(request)
    if verify is False:
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS, msg)
    person = Person.objects.filter(username=user_id).first()

    flightId = Flight.objects.filter(fid=flightId).first()
    airport = flightId.oriStat
    gate = DeparGate.objects.filter(depId=gate, airId=airport).first()

    if type == "商务舱" and flightId.cAvaSeat <= 0:
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS, "机票已定满")
    elif type == "经济舱" and flightId.eAvaSeat <= 0:
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS, "机票已定满")


    ticket_list = Ticket.objects.filter(flightId=flightId, seatId=seatId).count()
    if ticket_list > 0:
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS, "duplicate ticket")
    ticket = Ticket(flightId=flightId, seatId=seatId, gate=gate, type=type, price=price, passengerId=person,
                    saleTime=saleTime, detail=detail)
    ticket.save()

    return success_api_response({"msg": "succeed init ticket."})


@response_wrapper
@require_http_methods(['DELETE'])
@jwt_auth(perms=[TICKET_CHANGE])
def dlt_ticket_info(request: HttpResponse):
    """
        :param request: delete
               airline_id: int
        :return:
        """
    body: dict = parse_data(request)
    flightId = body['flight_id']
    seatId = body['seat_id']

    flightId = Flight.objects.filter(fid=flightId).first()
    verify, msg, user_id = verify_jwt_token(request)

    if verify is False:
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS, msg)

    person = Person.objects.filter(username=user_id).first()
    ticket_find = Ticket.objects.filter(flightId=flightId, seatId=seatId, passengerId=person)
    #print(ticket_find)
    if ticket_find.count() == 0:
        return failed_api_response(ErrorCode.ITEM_NOT_FOUND, "ticket not found.")
    Ticket.objects.filter(flightId=flightId, seatId=seatId).delete()
    return success_api_response({"msg": "succeed delete."})


@response_wrapper
@require_http_methods(['PATCH'])
@jwt_auth(perms=[TICKET_CHANGE])
def patch_ticket_info(request: HttpResponse):
    """
        :param flight_id: str
        :param request: PATCH
        :return:
         {
            "current_status": "等待",
            "depart_time": "07:00",
            "arrive_time": "09:12",
            "left_tickets": "89",
            "ontime": True
        }

        """
    body: dict = parse_data(request)
    flightId = body['flight_id']
    seatId = body['seat_id']
    gate_str = body['gate']
    flight = Flight.objects.filter(fid=flightId).first()

    ticket_find = Ticket.objects.filter(flightId=flight, seatId=seatId)
    #print(ticket_find)
    if ticket_find.count() == 0:
        return failed_api_response(ErrorCode.ITEM_NOT_FOUND, "ticket not found.")

    ticket = ticket_find.first()

    if gate_str is not None:
        airport = ticket.flightId.oriStat
        #print(gate_str)
        #print(airport)
        #print(DeparGate.objects.all())
        gate = DeparGate.objects.filter(depId=gate_str, airId=airport).first()
        #print(gate)
        ticket.gate = gate
        ticket.save()

    return success_api_response({"msg": "succeed recomposed."})


ticket_url = wrapped_api({
    "get": get_ticket_info,
    "post": init_ticket_info,
    "patch": patch_ticket_info,
    "delete": dlt_ticket_info
})
