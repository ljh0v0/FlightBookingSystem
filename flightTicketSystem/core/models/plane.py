from django.db import models
from core.models.permissions import (PLANE_CREATE, PLANE_CHANGE, PLANE_VIEW, PLANE_DELETE)

class Plane(models.Model):
    """
    id (django auto included)
    attTime    (date)
    mileage    (double/公里)
    ownedCpn   (frgKey -> Company)
    price      (double/万元)
    voyCnt     (int)
    seatCnt    (int) 
    """
    pid = models.CharField(max_length=10, primary_key=True, verbose_name="编号")
    attTime = models.DateField(verbose_name="服役时间")
    type = models.CharField(max_length=10, verbose_name="飞机型号", default="播音747")
    mileage = models.DecimalField(verbose_name="航程", max_digits=10, decimal_places=2)
    ownedCpn = models.ForeignKey(verbose_name="所属航空公司", to="Company", on_delete=models.CASCADE)
    price = models.DecimalField(verbose_name="购价", max_digits=10, decimal_places=2)
    voyCnt = models.IntegerField(verbose_name="出航次数", default=0)
    seatCnt = models.IntegerField(verbose_name="座位数", default=300) # 默认300座位
    type = models.CharField(max_length=20, verbose_name="飞机型号", default="波音737")
    class Meta:
        verbose_name = "飞机"
        default_permissions = ()
        permissions = [
            (PLANE_CREATE, PLANE_CREATE),
            (PLANE_CHANGE, PLANE_CHANGE),
            (PLANE_DELETE, PLANE_DELETE),
            (PLANE_VIEW, PLANE_VIEW)
        ]