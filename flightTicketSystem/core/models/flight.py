from django.db import models
from core.models.permissions import (FLIGHT_CREATE, FLIGHT_CHANGE, FLIGHT_VIEW, FLIGHT_DELETE)


class Flight(models.Model):
    """
    id          (char)
    status:     (char, choices)
    airline:    (frgKey -> Airline)
    plane:      (frgKey -> Plane)
    ownedCpn:   (frgKey -> Company)
    oriStat:    (frgKey -> Airport)
    destStat:   (frgKey -> Airport)
    onTime:     (bool)
    flyDate:    (Date)
    flyTime:    (Time)
    arvTime:    (Time)
    
    cprice: int
    eprice: int
    """
    STATUS_CHOICES = (
        ('W', '等待'),
        ('C', '检票中'),
        ('L', '晚点'),
        ('F', '飞行中'),
        ('A', '已到达'),
        ('D', '失联')
    )
    fid = models.CharField(max_length=10, verbose_name="航班编号")
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='W', verbose_name="状态")
    airline = models.ForeignKey(to="Airline", on_delete=models.CASCADE, verbose_name="所属航线")
    plane = models.ForeignKey(to="Plane", on_delete=models.PROTECT, verbose_name="所用飞机")
    ownedCpn = models.ForeignKey(to="Company", on_delete=models.CASCADE,
                                 verbose_name="所属公司")  # TODO plane and cpn has inner constraint
    oriStat = models.ForeignKey(to="Airport", on_delete=models.PROTECT, verbose_name="起始站", related_name="oriStat")
    destStat = models.ForeignKey(to="Airport", on_delete=models.PROTECT, verbose_name="终点站", related_name="destStat")
    onTime = models.BooleanField(verbose_name="是否准点")

    cAvaSeat = models.IntegerField(verbose_name="商务舱剩余座位数", default=300)  # 总票数/总座位数在飞机实体的属性中
    eAvaSeat = models.IntegerField(verbose_name="经济舱剩余座位数", default=300)

    flyDate = models.DateField(verbose_name="飞行日期")
    flyTime = models.TimeField(verbose_name="起飞时间")
    arvTime = models.TimeField(verbose_name="到达时间")
    
    cprice = models.IntegerField(verbose_name="商务舱原价")
    eprice = models.IntegerField(verbose_name="经济舱原价")
    
    class Meta:
        verbose_name = "航班"
        default_permissions = ()
        permissions = [
            (FLIGHT_CREATE, FLIGHT_CREATE),
            (FLIGHT_CHANGE, FLIGHT_CHANGE),
            (FLIGHT_DELETE, FLIGHT_DELETE),
            (FLIGHT_VIEW, FLIGHT_VIEW)
        ]
        unique_together = (("fid", "ownedCpn", "flyDate")) # 同一fid可以对应不同的飞行日期，不同航空公司允许有相同fid
