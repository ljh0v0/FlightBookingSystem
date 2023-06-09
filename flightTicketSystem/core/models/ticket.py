from django.db import models
from core.models.permissions import (TICKET_CREATE, TICKET_CHANGE, TICKET_VIEW, TICKET_DELETE)

class Ticket(models.Model):
    """
    """
    SEAT_TYPE = (
        ('E', "经济舱"),
        ('C', "商务舱")
    )
    flightId = models.ForeignKey(to="Flight", on_delete=models.CASCADE, verbose_name="所属航班")
    seatId = models.CharField(max_length=10, verbose_name="座位号")
    gate = models.ForeignKey(to="DeparGate", on_delete=models.SET_NULL, verbose_name="登机口", null=True)
    type = models.CharField(max_length=10, default='E', choices=SEAT_TYPE, verbose_name="类型")
    price = models.DecimalField(max_digits=6, decimal_places=1, verbose_name="票价")
    passengerId = models.ForeignKey(to="Person", on_delete=models.CASCADE, verbose_name="乘客")
    saleTime = models.DateTimeField(verbose_name="出票时间")
    detail = models.TextField(verbose_name="细节") # 如行李信息、餐食等

    class Meta:
        unique_together = (("flightId", "seatId"))
        verbose_name = "机票"
        default_permissions = ()
        permissions = [
            (TICKET_CREATE, TICKET_CREATE),
            (TICKET_CHANGE, TICKET_CHANGE),
            (TICKET_DELETE, TICKET_DELETE),
            (TICKET_VIEW, TICKET_VIEW)
        ]
