from typing import Any

from django.db.models import IntegerChoices
from rest_framework.response import Response


class Errcode(IntegerChoices):
    # 通用错误码
    CONTINUE = 2, 'Continue'
    SUCCESS = 1, 'Success'
    DONE = 0, 'Done'
    FAIL = -1, 'Fail'

    # 客户端侧错误
    MISSING_PARAMS = -40001, '缺少参数，或参数为空值'
    INVALID_PARAMS = -40002, '提供了错误的参数值'
    INVALID_CERTIFICATE = -40003, '鉴权凭证不合法'
    RESOURCE_NOT_FOUND = -40004, '资源未找到'
    CACHE_MAY_EXPIRED = -40005, '请求非法，或缓存已失效'

    # 服务端侧错误
    WIP = -50001, '接口正在开发'
    FAIL_LOGOUT = -50002, '登出失败'


def wrap200(response: Response, code: Errcode) -> Response:
    """
    如果响应内容不符合标准格式，则封装为标准格式。

    :param response: 原始响应。
    :param code: 从 ``request`` 中推断的错误代码。
    :return: 符合标准格式的响应。
    """
    if not isinstance(response.data, dict) or len({'code', 'message', 'data'} - set(response.data.keys())) > 0:
        response.data = resp(response.data, code=code)

    return response


def resp200(data: Any = None, code: Errcode = Errcode.FAIL, msg: str = None, **kwargs: Any) -> Response:
    """
    构造标准格式的响应。

    :param data: 要返回的数据，默认为空。
    :param code: 自定义响应码，默认为失败。
    :param msg: 响应消息。不提供则默认为 ``code`` 的标签。
    :return: DRF 的响应类对象。
    """
    data = resp(data, code, msg, **kwargs)
    return Response(data)


def resp(data: Any = None, code: Errcode = Errcode.FAIL, msg: str = None, **kwargs: Any) -> dict:
    """
    构造标准响应格式。

    :param data: 要返回的数据，默认为空。
    :param code: 自定义响应码，默认为失败。
    :param msg: 响应消息。不提供则默认为 ``code`` 的标签。
    :return: 一个字典。
    """
    data = {
        'code': code.value,
        'message': msg or code.label,
        'data': data,
        **kwargs,
    }
    if 'error' in data and data['error'] is None:
        _ = data.pop('error')

    assert 'data' in data
    assert 'code' in data and type(data['code']) is int
    assert 'message' in data and type(data['message']) is str
    return data
