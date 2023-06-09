"""
define the url routes of core api
"""
from django.urls import path

from core.api.airline import airline_detail_url, airline_url
from core.api.airport import airport_detail_url, airport_url
from core.api.airport_date import get_cpn_total, get_on_time, get_flow
from core.api.city import city_detail_url, city_url
from core.api.company import cpn_detail_url, cpn_url
from core.api.flight import flight_detail_url, flight_url
from core.api.gate import gate_url
from core.api.person import person_detail_url, person_url, person_token_url
from core.api.ticket import ticket_url
from core.api.login import create_user, user_logout, add_permission
from core.api.auth import obtain_jwt_token
from core.api.plane import plane_url
from core.api.worker import worker_url, relation_url

urlpatterns = [
    path('api/core/airline/<str:airline_id>', airline_detail_url),
    path('api/core/airline', airline_url),
    path('api/core/airport/<str:airport_id>', airport_detail_url),
    path('api/core/airport', airport_url),
    path('api/core/city/<str:city_id>', city_detail_url),
    path('api/core/city', city_url),
    path('api/core/company/<str:acro_name>', cpn_detail_url),
    path('api/core/company', cpn_url),
    path('api/core/flight/<str:flight_id>', flight_detail_url),
    path('api/core/flight', flight_url),
    path('api/core/user/<str:user_id>', person_detail_url),
    path('api/core/user', person_url),
    path('api/core/trip_record', ticket_url),
    path('api/core/plane', plane_url),
    path('api/core/gate', gate_url),
    path('api/core/check', person_token_url),

    path('api/core/worker', worker_url),
    path('api/core/relation', relation_url),

    path('api/core/airport_cpn', get_cpn_total),
    path('api/core/airport_ontime', get_on_time),
    path('api/core/airport_flow', get_flow),

    path('api/login', obtain_jwt_token),
    path('api/logout', user_logout),
    path('api/register', create_user),
    path('api/permission', add_permission)
]
