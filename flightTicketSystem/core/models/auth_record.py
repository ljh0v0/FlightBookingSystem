"""
declare Auth Record model
"""

from django.contrib.auth import get_user_model
from django.db import models
from flightTicketSystem.settings import AUTH_USER_MODEL


class AuthRecord(models.Model):
    """This model describes a user auth record
    """
    user = models.ForeignKey(to=AUTH_USER_MODEL, on_delete=models.CASCADE)
    login_at = models.DateTimeField()
    expires_by = models.DateTimeField()

    class Meta:
        # no permissions needed
        default_permissions = ()
