from core.models.flight import Flight
from django.db import models
from core.models.permissions import (STEWARD_CREATE, STEWARD_CHANGE, STEWARD_VIEW, STEWARD_DELETE)

class Steward(models.Model):
    """
    wid     (django auto included)
    pid     (frgKey -> Person)
    servTime (float /h)
    ownedCpn (frgKey -> Company)
    empDate  (date)
    pos     (char, choices)
    """

    pid = models.ForeignKey(to="Person", on_delete=models.PROTECT, verbose_name="身份证号")
    servTime = models.FloatField(verbose_name="空中服务时间") 
    ownedCpn = models.ForeignKey(to="Company", on_delete=models.CASCADE, verbose_name="所属公司")
    empDate = models.DateField(verbose_name="入职时间")
    JOB_TYPE = (
        ('S', "乘务长"),
        ('J', "乘务员")
    )
    pos = models.CharField(choices=JOB_TYPE, max_length=10, verbose_name="职务")

    flight = models.ManyToManyField(to="Flight", verbose_name="航班乘务员关系表", through="StewardFlight")

    def __str__(self):
        pass

    class Meta:
        # db_table = ''
        managed = True
        verbose_name = "空乘人员"
        default_permissions = ()
        permissions = [
            (STEWARD_CREATE, STEWARD_CREATE),
            (STEWARD_CHANGE, STEWARD_CHANGE),
            (STEWARD_DELETE, STEWARD_DELETE),
            (STEWARD_VIEW, STEWARD_VIEW)
        ]

class StewardFlight(models.Model):
    steward = models.ForeignKey(to="Steward", on_delete=models.CASCADE)
    flight = models.ForeignKey(to="Flight", on_delete=models.CASCADE)