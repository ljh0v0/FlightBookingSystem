from django.db import models
from core.models.permissions import (DEPAR_GATE_CREATE, DEPAR_GATE_CHANGE, DEPAR_GATE_VIEW, DEPAR_GATE_DELETE)

class DeparGate(models.Model):
    """
    depId 
    airId
    """
    depId = models.CharField(max_length=8, default='A')
    airId = models.ForeignKey(to="Airport", on_delete=models.CASCADE, verbose_name="所在机场")

    class Meta:
        unique_together = (("depId", "airId"))
        verbose_name = "登机口"
        default_permissions = ()
        permissions = [
            (DEPAR_GATE_CREATE, DEPAR_GATE_CREATE),
            (DEPAR_GATE_CHANGE, DEPAR_GATE_CHANGE),
            (DEPAR_GATE_DELETE, DEPAR_GATE_DELETE),
            (DEPAR_GATE_VIEW, DEPAR_GATE_VIEW)
        ]

