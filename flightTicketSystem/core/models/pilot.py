from django.db import models
from core.models.permissions import (PILOT_CREATE, PILOT_CHANGE, PILOT_VIEW, PILOT_DELETE)

class Pilot(models.Model):
    """
    wid     (django auto included)
    pid     (frgKey -> Person)
    flyTime (float /h)
    ownedCpn (frgKey -> Company)
    empDate  (date)
    pos     (char, choices)
    """

    pid = models.ForeignKey(to="Person", on_delete=models.PROTECT, verbose_name="身份证号")
    flyTime = models.FloatField(verbose_name="飞行时间") 
    ownedCpn = models.ForeignKey(to="Company", on_delete=models.CASCADE, verbose_name="所属公司")
    empDate = models.DateField(verbose_name="入职时间")
    JOB_TYPE = (
        ('S', "机长"),
        ('J', "副机长")
    )
    pos = models.CharField(choices=JOB_TYPE, max_length=10, verbose_name="职务")

    flight = models.ManyToManyField(to="Flight", verbose_name="航班飞行员关系表", through="PilotFlight")

    def __str__(self):
        pass

    class Meta:
        # db_table = ''
        managed = True
        verbose_name = "飞行人员"
        default_permissions = ()
        permissions = [
            (PILOT_CREATE, PILOT_CREATE),
            (PILOT_CHANGE, PILOT_CHANGE),
            (PILOT_DELETE, PILOT_DELETE),
            (PILOT_VIEW, PILOT_VIEW)
        ]

class PilotFlight(models.Model):
    pilot = models.ForeignKey(to="Pilot", on_delete=models.CASCADE)
    flight = models.ForeignKey(to="Flight", on_delete=models.CASCADE)
