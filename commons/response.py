__all__ = [
    'Errcode',
    'resp200',
    'wrap200',
]

from typing import Any

from django.db.models import IntegerChoices
from rest_framework.response import Response


class Errcode(IntegerChoices):
    """
    错误码。

    - 项目定义的错误码，出现在 HTTP 响应数据内，用于前端及接口调用方识别 API 响应状态。
    - 数值已超出 16 位有符号整数范围，如需存储，至少需要 32 位有符号整数。
    """

    # 通用错误码
    CONTINUE = 2, '继续'
    SUCCESS = 1, '成功'
    DONE = 0, '完成'
    FAIL = -1, '失败'

    # 客户端侧错误
    MISSING_PARAMS = -40001, '缺少参数，或参数为空值'
    INVALID_PARAMS = -40002, '提供了错误的参数值'
    INVALID_CERTIFICATE = -40003, '鉴权凭证不合法'
    RESOURCE_NOT_FOUND = -40004, '资源未找到'
    CACHE_MAY_EXPIRED = -40005, '请求非法，或缓存已失效'
    INVALID_REFRESH_TOKEN = -40006, '刷新令牌已失效'
    INVALID_ACCESS_TOKEN = -40007, '访问令牌已失效'
    AUTHENTICATION_UNSUPPORTED = -40008, '认证方式不受支持'
    AUTHORIZATION_TERMINATED = -40009, '授权流程被终止'

    # 服务端侧错误
    WIP = -50001, '接口正在开发'
    FAIL_LOGOUT = -50002, '登出失败'
    APP_NOT_FOUND = -50003, '应用不存在'

    # 授权鉴权服务侧错误
    FAIL_AUTHORIZATION = -70001, '授权失败'
    FAIL_OBTAIN_OPENID = -70002, 'OpenID 获取失败'
    FAIL_EXCHANGE_TOKEN = -70003, '访问令牌交换失败'
    FAIL_OBTAIN_PROFILES = -70004, '用户资料获取失败'
    WRONG_ACCOUNT_TYPE = -70005, '账号类型错误（不是一个用户）'


def _standardize(data: Any = None, code: Errcode = Errcode.FAIL, msg: str = None, **kwargs: Any) -> dict:
    """
    构造标准的响应数据格式。

    :param data: 要返回的业务数据部分，默认为空。
    :param code: 错误代码，默认为失败。
    :param msg: 错误提示。不提供则默认为 ``code`` 的标签。
    :return: 一个字典。
    """
    body = {
        'code': code.value,
        'message': msg or code.label,
        'data': data,
        **kwargs,
    }
    if 'error' in body and body['error'] is None:
        _ = body.pop('error')

    assert 'data' in body, 'API响应缺少 "data" 字段。'
    assert 'code' in body, 'API响应缺少 "code" 字段。'
    assert 'message' in body, 'API响应缺少 "message" 字段。'
    assert type(body['code']) is int, 'API响应的 "code" 字段必须是 int 类型。'
    assert type(body['message']) is str, 'API响应的 "message" 字段必须是 str 类型。'
    assert body['message'], 'API响应的 "message" 字段不允许为空字符串。'
    if 'pages' in body:
        assert type(body['pages']) is int, 'API响应的 "pages" 字段必须是 int 类型。'
    return body


def resp200(data: Any = None, code: Errcode = Errcode.FAIL, msg: str = None, **kwargs: Any) -> Response:
    """
    构造标准格式的响应。

    HTTP 响应状态码固定为 `200 OK <https://developer.mozilla.org/zh-CN/docs/Web/HTTP/Status/200>`_ 。

    标准响应格式为一个JSON对象，必定包含以下字段：

    - ``code`` 表示错误代码，必定为 integer（int32）。
    - ``message`` 表示错误提示，必定为 string 且不为空字符串，不应存在换行符，不建议以句号结尾。
    - ``data`` 表示业务数据，必定存在，但可以为 ``null`` 或其它任意类型。

    可能包含以下字段：

    - ``prev`` 表示上一页的单个请求 URL，可以为 string 或 ``null``，不为空字符串。
    - ``next`` 表示下一页的单个请求 URL，可以为 string 或 ``null``，不为空字符串。
    - ``pages`` 表示总页数，必定为 integer（int64）。
    - ``error`` 表示需要提供给外部的内部错误，一般为序列化器校验器产生的嵌套数组或嵌套对象，但也可以是其它任意类型。

    :param data: 要返回的业务数据部分，默认为空。
    :param code: 错误代码，默认为失败。
    :param msg: 错误提示。不提供则默认为 ``code`` 的标签。
    :return: DRF 响应对象 :class:`Response` 。
    """
    body = _standardize(data, code, msg, **kwargs)
    return Response(body)


def wrap200(response: Response, code: Errcode) -> Response:
    """
    如果响应内容不符合标准格式，则封装为标准格式。

    :param response: 原始响应。
    :param code: 从 ``request`` 中推断的错误代码。
    :return: 符合标准格式的响应。
    """
    if not isinstance(response.data, dict) or len({'code', 'message', 'data'} - set(response.data.keys())) > 0:
        response.data = _standardize(response.data, code=code)

    return response
