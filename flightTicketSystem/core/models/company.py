from django.db import models
from core.models.permissions import (COMPANY_CREATE, COMPANY_CHANGE, COMPANY_VIEW, COMPANY_DELETE)


class Company(models.Model):
    """
    acroName:   (priKey, char)
    fullName:   (char)
    icon:       (char[url])
    onRate:     (double)
    """

    acroName = models.CharField(primary_key=True, max_length=8, verbose_name="缩写")
    fullName = models.CharField(max_length=50, verbose_name="全称")
    icon = models.URLField(max_length=50, verbose_name="图标", null=True)
    onRate = models.DecimalField(verbose_name="正点率", max_digits=4, decimal_places=2)

    airport = models.ManyToManyField(to="Airport", verbose_name="机场航空公司关系表", through='CompanyAirport')

    class Meta:
        verbose_name = "航空公司"
        default_permissions = ()
        permissions = [
            (COMPANY_CREATE, COMPANY_CREATE),
            (COMPANY_CHANGE, COMPANY_CHANGE),
            (COMPANY_DELETE, COMPANY_DELETE),
            (COMPANY_VIEW, COMPANY_VIEW)
        ]


class CompanyAirport(models.Model):
    airport = models.ForeignKey(to="Airport", on_delete=models.CASCADE)
    company = models.ForeignKey(to="Company", on_delete=models.CASCADE)
