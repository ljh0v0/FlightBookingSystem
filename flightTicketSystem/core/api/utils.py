"""
utils for generating api responses
"""
import json
import re
from enum import Enum, unique

from django.db import models
from django.http import HttpRequest, JsonResponse
from django.views.decorators.http import require_http_methods


@unique
class ErrorCode(Enum):
    """
    api error code enumeration
    """

    # success code family
    SUCCESS = 200  # deprecated
    SUCCESS_CODE = 200_00

    # bad request family
    INVALID_REQUEST_ARGS = 400  # deprecated
    BAD_REQUEST_ERROR = 400_00
    INVALID_REQUEST_ARGUMENT_ERROR = 400_01
    REQUIRED_ARG_IS_NULL_ERROR = 400_02

    # unauthorized family
    UNAUTHORIZED = 401  # deprecated
    UNAUTHORIZED_ERROR = 401_00

    # refuse family
    REFUSE_ACCESS = 403  # deprecated
    REFUSE_ACCESS_ERROR = 403_00
    CONFIRM_CHECK_OUT = 403_01
    SEAT_ARRANGEMENT_ERROR = 403_02

    # not found family
    ITEM_NOT_FOUND = 404  # deprecated
    NOT_FOUND_ERROR = 404_00
    ACTIVE_FLIGHT_NOT_FOUND_ERROR = 404_01  # currently no exactly flight

    # duplicated family
    ITEM_ALREADY_EXISTS = 409  # deprecated
    DUPLICATED_ERROR = 409_00

    PERSON_NOT_FOUND = 520_00


class SetType(Enum):
    """
    the argument named type for PUT
    if not in these, the int mean the id of model
    """
    SET_NONE = -1
    NONE = 0


def _api_response(success, data) -> dict:
    """
    wrap an api response dict obj
    :param success: whether the request is handled successfully
    :param data: requested data
    :return: a dictionary object, like {'success': success, 'data': data}
    """
    return {"success": success, "data": data}


def failed_api_response(code, error_msg=None) -> dict:
    """
    wrap an failed response dict obj
    :param code: error code, refers to ErrorCode, can be an integer or a str (error name)
    :param error_msg: external error information
    :return: an api response dictionary
    """
    if isinstance(code, str):
        code = ErrorCode[code]
    if isinstance(code, int):
        code = ErrorCode(code)
    assert isinstance(code, ErrorCode)
    assert isinstance(code.value, int)

    if code.value < 1000:
        # using simple http status code is deprecated
        import warnings
        warnings.warn("using simple http code {} is deprecated".format(code.name))
        code = ErrorCode(code.value * 100)  # set to new style error code

    assert code.value >= 10000

    if error_msg is None:
        error_msg = str(code)
    else:
        error_msg = str(code) + ': ' + error_msg

    status_code = code.value // 100
    detailed_code = code.value
    return _api_response(
        success=False,
        data={
            "code": status_code,
            "detailed_error_code": detailed_code,
            "error_msg": error_msg
        })


def success_api_response(data) -> dict:
    """
    wrap a success response dict obj
    :param data: requested data
    :return: an api response dictionary
    """
    return _api_response(True, data)


def response_wrapper(func):
    """
    decorate a given api-function, parse its return value from a dict to a HttpResponse
    :param func: a api-function
    :return: wrapped function
    """

    def _inner(*args, **kwargs):
        _response = func(*args, **kwargs)
        if isinstance(_response, dict):
            if _response['success']:
                _response = JsonResponse(_response['data'])
            else:
                status_code = _response.get("data").get("code")
                _response = JsonResponse(_response['data'])
                _response.status_code = status_code
        return _response

    return _inner


def wrapped_api(api_dict: dict):
    """
    wrap apis together with 4 methods(get/post/put/delete)
    :param api_dict: dict as {'get': get_api, 'post': post_api ...}
    :return: a api
    """
    assert isinstance(api_dict, dict)
    api_dict = {k.upper(): v for k, v in api_dict.items()}
    assert set(api_dict.keys()).issubset(['GET', 'POST', 'PUT', 'DELETE', 'PATCH'])

    @require_http_methods(api_dict.keys())
    def _api(request, *args, **kwargs):
        return api_dict[request.method](request, *args, **kwargs)

    return _api


def parse_data(request: HttpRequest):
    """Parse request body and generate python dict

    Args:
        request (HttpRequest): all http request

    Returns:
        | request body is malformed = None
        | otherwise                 = python dict
    """
    try:
        return json.loads(request.body.decode())
    except json.JSONDecodeError:
        return None

def require_item_exist(model: models.Model, field: str, item: str):
    """Check if the query item is existed

    Args:
        model (models.Model): query model
        field (str): query field
        item  (str): the same as parameter name defined in urls.py

    example:

    @response_wrapper
    @require_GET
    @require_item_exist(model, "model_id", "id")
    def model_get(request: HttpRequest, model_id: int) -> dict:
    """
    def decorator(func):
        def wrapper(request: HttpRequest, *args, **kwargs):
            item_id = kwargs.get(item)
            kwargs.pop(item, None)
            if not model.objects.filter(**{field: item_id}).exists():
                return failed_api_response(ErrorCode.ITEM_NOT_FOUND)
            return func(request, item_id, *args, **kwargs)
        return wrapper
    return decorator


def require_item_miss(model: models.Model = None, field: str = None, func=None):
    """Check if the query item is NOT duplicated

    NEVER use it before validate_args

    Args:
        model (models.Model, optional): query model. Defaults to None.
        field (str, optional): query field. Defaults to None.
        func (Callable, optional): custom check function. Defaults to None.

    example:

    @response_wrapper
    @require_POST
    @validate_args(model=model)
    @require_item_miss(request: HttpRequest) -> dict:
    """
    def decorator(function):
        def wrapper(request: HttpRequest, *args, **kwargs):
            if func is None:
                data: dict = parse_data(request)
                item_id = data.get(field)
                if not model.objects.filter(**{field: item_id}).exists():
                    return function(request, *args, **kwargs)
            elif func(request, *args, **kwargs):
                return function(request, *args, **kwargs)
            return failed_api_response(ErrorCode.ITEM_ALREADY_EXISTS)
        return wrapper
    return decorator


def default_checker(request: HttpRequest, model: models.Model, exclude: list) -> bool:
    """Default checker for argument validation

    Args:
        request (HttpRequest): all http request
        model (models.Model): query model
        exclude (list): optional fields

    Returns:
        bool: indicate if the argument is valid
    """
    data: dict = parse_data(request)
    # if fails
    if data is None or not isinstance(data, dict):
        return False

    if exclude is None:
        exclude = []

    # use private field, but relatively stable
    fields = [field.name for field in model._meta.get_fields()]
    for key in data.keys():
        if not key in fields and key not in exclude:
            return False

    return True


def validate_args(model: models.Model = None, exclude: list = None, func=None):
    """validate argument

    Args:
        model (models.Model, optional): query model. Defaults to None.
        exclude (list[str], optional): optional fields. Defaults to None.
        func (Callable, optional): custom check function. Defaults to None.

    Returns:
        [type]: [description]
    """
    def decorator(function):
        def wrapper(request, *args, **kwargs):
            validation = False
            if func is None:
                validation = default_checker(request, model, exclude)
            else:
                validation = func(request)
            if validation:
                return function(request, *args, **kwargs)
            return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS)
        return wrapper
    return decorator


def username_checker(username: str):
    """username checker

    Args:
        username (str): username input by client

    Returns:
        bool: indicate if the username is legal
    """
    legal_username = '^[a-z0-9_]+$' # only lower case letters, digit, underscore are allowed
    if re.match(legal_username, username, flags=0) is None:
        return False
    if username.isdigit(): # username cannot be pure digit
        return False
    return True
