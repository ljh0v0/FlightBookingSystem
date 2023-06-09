from django.db import models
from core.models.permissions import (AIRPORT_CREATE, AIRPORT_CHANGE, AIRPORT_VIEW, AIRPORT_DELETE)


class Airport(models.Model):
    """
    name    (char)
    airId      (int, priKey)
    cityId  (frgKey&priKey -> City)
    attTime (date)
    address (char)
    """
    airId = models.CharField(max_length=10, primary_key=True, verbose_name="机场编号")
    cityId = models.ForeignKey(to="City", verbose_name="所在城市", on_delete=models.CASCADE)
    name = models.CharField(max_length=50, verbose_name="机场名")
    attTime = models.DateField(verbose_name="投入时间")
    address = models.TextField(verbose_name="地址")

    class Meta:
        verbose_name = "机场"
        default_permissions = ()
        permissions = [
            (AIRPORT_CREATE, AIRPORT_CREATE),
            (AIRPORT_CHANGE, AIRPORT_CHANGE),
            (AIRPORT_DELETE, AIRPORT_DELETE),
            (AIRPORT_VIEW, AIRPORT_VIEW)
        ]
