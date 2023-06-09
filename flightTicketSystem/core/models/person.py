from django.db import models
from django.contrib.auth.models import AbstractUser
from core.models.permissions import (PERSON_CREATE, PERSON_CHANGE, PERSON_VIEW, PERSON_DELETE)

class Person(AbstractUser):
    # username -> phone number
    # user = models.OneToOneField(User, on_delete=models.CASCADE)
    id = models.CharField(max_length=18, primary_key=True, verbose_name="身份证号")
    sex = models.CharField(max_length=1, choices=(('M', '男'), ('F', '女')), null=False)
    upor = models.CharField(max_length=100, verbose_name="常住地", null=True)
    name = models.CharField(max_length=30, verbose_name="姓名")
    birthday = models.DateField(verbose_name="生日", null=True)
    auth = models.BooleanField(verbose_name="权限",null = False, default=True)
    
    class Meta(AbstractUser.Meta):
        #swappable = 'AUTH_USER_MODEL'
        #app_label = 'core'
        verbose_name = "人"
        default_permissions = ()
        permissions = [
            (PERSON_CREATE, PERSON_CREATE),
            (PERSON_CHANGE, PERSON_CHANGE),
            (PERSON_DELETE, PERSON_DELETE),
            (PERSON_VIEW, PERSON_VIEW)
        ]