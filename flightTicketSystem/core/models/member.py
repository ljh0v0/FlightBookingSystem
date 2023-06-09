from django.db import models
from core.models.permissions import (MEMBER_CREATE, MEMBER_CHANGE, MEMBER_VIEW, MEMBER_DELETE)

class Member(models.Model):
    """
    """
    AUTH = (
        ('N', "普通用户"),
        ('M', "管理员")
    )
    pid = models.ForeignKey(to="Person", on_delete=models.CASCADE, verbose_name="身份证号")
    account = models.CharField(primary_key=True, max_length=11, verbose_name="账号/手机号")
    password = models.CharField(max_length=100, null=False, verbose_name="密码")
    authority = models.CharField(choices=AUTH, default='N', max_length=1, verbose_name="用户权限")

    class Meta:
        verbose_name = "用户"
        default_permissions = ()
        permissions = [
            (MEMBER_CREATE, MEMBER_CREATE),
            (MEMBER_CHANGE, MEMBER_CHANGE),
            (MEMBER_DELETE, MEMBER_DELETE),
            (MEMBER_VIEW, MEMBER_VIEW)
        ]