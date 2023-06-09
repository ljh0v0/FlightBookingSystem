from django.db import models
from django.db.models import constraints
from core.models.permissions import (TICKET_INFO_CREATE, TICKET_INFO_CHANGE, TICKET_INFO_VIEW, TICKET_INFO_DELETE)

class TicketInfo(models.Model):
    """
    flightId: frgKey -> Flight
    type:   char
    detail: text
    leftTicket: int
    totalTicket: int
    discount: [0,1]
    """
    flightId = models.ForeignKey(to="Flight", verbose_name="对应航班", on_delete=models.CASCADE)
    type = models.CharField(max_length=10, verbose_name="航舱类型") # "经济舱" (前端插入时提供折扣，由后端处理后存入db)
    detail = models.TextField(verbose_name="备注说明")
    leftTicket = models.SmallIntegerField(verbose_name="剩余票数") # 每次购票，该值-1
    totalTicket = models.SmallIntegerField(verbose_name="总票数", editable=False) # 插入后不得修改 (插入者/触发器保证同航班的所有票务的总票数不超过实际座位数)
    discount = models.DecimalField(max_digits=2, decimal_places=1, default=1, verbose_name="折扣") # 默认无折扣

    class Meta:
        verbose_name = "航班票务信息"
        constraints = [
            models.UniqueConstraint(fields=["flightId", "type", "discount"], name="unique_ticket_info"),
            models.CheckConstraint(check=models.Q(discount__gt=0) & models.Q(discount__lte=1), name="discount__in__01")
        ]
        unique_together = (("flightId", "type", "discount"))
        default_permissions = ()
        permissions = [
            (TICKET_INFO_CREATE, TICKET_INFO_CREATE),
            (TICKET_INFO_CHANGE, TICKET_INFO_CHANGE),
            (TICKET_INFO_DELETE, TICKET_INFO_DELETE),
            (TICKET_INFO_VIEW, TICKET_INFO_VIEW)
        ]
