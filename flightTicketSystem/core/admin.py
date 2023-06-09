from django.contrib import admin

# Register your models here.

from core.models.airline import Airline
from core.models.airport import Airport
from core.models.auth_record import AuthRecord
from core.models.city import City
from core.models.company import Company, CompanyAirport
from core.models.deparGate import DeparGate
from core.models.flight import Flight
from core.models.member import Member
from core.models.person import Person
from core.models.pilot import Pilot, PilotFlight
from core.models.plane import Plane
from core.models.steward import Steward, StewardFlight
from core.models.ticket_info import TicketInfo
from core.models.ticket import Ticket

admin.site.register(Airline)
admin.site.register(Airport)
admin.site.register(AuthRecord)
admin.site.register(City)
admin.site.register(Company)
admin.site.register(CompanyAirport)
admin.site.register(DeparGate)
admin.site.register(Flight)
admin.site.register(Member)
admin.site.register(Person)
admin.site.register(Pilot)
admin.site.register(PilotFlight)
admin.site.register(Plane)
admin.site.register(Steward)
admin.site.register(StewardFlight)
admin.site.register(TicketInfo)
admin.site.register(Ticket)
