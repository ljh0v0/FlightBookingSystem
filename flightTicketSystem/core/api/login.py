from django.contrib import auth
from django.contrib.auth.models import Permission, User

from django.shortcuts import render, HttpResponse, redirect

from core.api.auth import jwt_auth
from core.api.utils import success_api_response, failed_api_response, ErrorCode, parse_data, response_wrapper
from core.models.permissions import PERSON_CHANGE
from core.models.ticket import TICKET_CREATE, TICKET_DELETE, TICKET_CHANGE
from core.models.person import Person

"""
args:
    id = models.CharField(max_length=18, primary_key=True, verbose_name="身份证号")
    sex = models.CharField(max_length=1, choices=(('M', '男'), ('F', '女')), null=False)
    upor = models.CharField(max_length=100, verbose_name="常住地")
    name = models.CharField(max_length=30, verbose_name="姓名")
"""

@response_wrapper
def create_user(request: HttpResponse):
    body: dict = parse_data(request)
    print(body)
    id = body['id']
    sex = body['sex']
    upor = body['upor']
    name = body['name']
    birthday = body['birth']
    password = body['password']
    username = body['phone']
    #permission_all = Permission.objects.all()
    num = Person.objects.filter(username=username).count()
    if num != 0:
        return failed_api_response(ErrorCode.ITEM_ALREADY_EXISTS, "用户名已存在")

    person = Person.objects.create_user(id=id, sex=sex, upor=upor, 
        name=name, birthday=birthday, password=password,username=username,auth = False)

    #print(person.get_all_permissions())

    permission_4 = Permission.objects.get(codename="创建机票")
    person.user_permissions.add(permission_4)
    permission_4 = Permission.objects.get(codename="删除机票")
    person.user_permissions.add(permission_4)
    permission_4 = Permission.objects.get(codename="查看机票")
    person.user_permissions.add(permission_4)
    permission_4 = Permission.objects.get(codename="修改机票")
    person.user_permissions.add(permission_4)

    #print(person.get_all_permissions())
    #print(person.has_perms(["core.修改机票"]))

    data = {
        "msg": "success register"
    }
    return success_api_response(data)


@response_wrapper
#@jwt_auth(perms=[PERSON_CHANGE])  ##################################################################################
def add_permission(request: HttpResponse):
    """
    :param request:
    :return:
    {
        "phone" : "123456"
    }
    """
    body: dict = parse_data(request)
    username = body['phone']

    num = Person.objects.filter(username=username)
    if num.count() == 0:
        return failed_api_response(ErrorCode.ITEM_NOT_FOUND, "用户不存在")

    person = num.first()

    person.auth = True
    person.save()
    permission_all = Permission.objects.all()
    for perm in permission_all:
        person.user_permissions.add(perm)
    data = {
        "msg": "success add permission"
    }
    return success_api_response(data)


"""
args:
    NONE
return:
    next path
"""


@response_wrapper
def user_logout(request):
    auth.logout(request)
    data = {
        "msg": "success logout"
    }
    return success_api_response(data)


"""
args:
    old_password
    new_password
    repeat_password
return:
    next path
"""


@response_wrapper
def set_password(request):
    user = request.user
    err_msg = ''
    old_password = request.POST.get('old_password', '')
    new_password = request.POST.get('new_password', '')
    repeat_password = request.POST.get('repeat_password', '')
    # 检查旧密码是否正确
    if Person.check_password(old_password):
        if not new_password:
            err_msg = '新密码不能为空'
            return failed_api_response(ErrorCode.CONFIRM_CHECK_OUT, err_msg)
        elif new_password != repeat_password:
            err_msg = '两次密码不一致'
            return failed_api_response(ErrorCode.CONFIRM_CHECK_OUT, err_msg)
        else:
            Person.set_password(new_password)
            Person.save()
            return success_api_response({"msg": "succeed"})
    else:
        err_msg = '原密码输入错误'
    content = {
        'err_msg': err_msg,
    }
    return failed_api_response(ErrorCode.CONFIRM_CHECK_OUT, err_msg)

# return ? next path / true/false
