from django.db import models
from core.models.permissions import (AIRLINE_CREATE, AIRLINE_CHANGE, AIRLINE_VIEW, AIRLINE_DELETE)
from core.models.city import City


class Airline(models.Model):
    """
    id (django auto included)
    oriCity:    (frgKey -> City)
    destCity:   (frgKey -> City)
    height:     (decimal/km)
    timeSect:   飞行时段可暂不考虑    TODO
    """
    # 在一个表中多次引用某个外键表，而且没有指定唯一的related_name会报错
    id = models.CharField(max_length=20, verbose_name="航线编号", primary_key=True)
    oriCity = models.ForeignKey(to="City", related_name="oriCity", on_delete=models.CASCADE, verbose_name="始发地")
    destCity = models.ForeignKey(to="City", related_name="destCity", on_delete=models.CASCADE, verbose_name="目的地")
    height = models.FloatField(verbose_name="飞行高度")

    class Meta:
        verbose_name = "航线"
        default_permissions = ()
        permissions = [
            (AIRLINE_CREATE, AIRLINE_CREATE),
            (AIRLINE_CHANGE, AIRLINE_CHANGE),
            (AIRLINE_DELETE, AIRLINE_DELETE),
            (AIRLINE_VIEW, AIRLINE_VIEW)
        ]
