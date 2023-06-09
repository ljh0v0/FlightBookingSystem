from django.db import models
from core.models.permissions import (CITY_CREATE, CITY_CHANGE, CITY_VIEW, CITY_DELETE)


class City(models.Model):
    """
    """
    id = models.CharField(primary_key=True, max_length=8, verbose_name="城市简拼")
    name = models.CharField(max_length=20, verbose_name="城市名")
    longitude = models.DecimalField(decimal_places=2, max_digits=5, verbose_name="经度")  # xx'xx''
    latitude = models.DecimalField(decimal_places=2, max_digits=5, verbose_name="纬度")
    province = models.CharField(max_length=8, verbose_name="所在省份")

    class Meta:
        verbose_name = "城市"
        default_permissions = ()
        permissions = [
            (CITY_CREATE, CITY_CREATE),
            (CITY_CHANGE, CITY_CHANGE),
            (CITY_DELETE, CITY_DELETE),
            (CITY_VIEW, CITY_VIEW)
        ]
