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

    - 标准的 API 响应状态码，出现在 HTTP 响应数据内，主要用于调用方识别、反馈 API 响应结果。
    - 单个错误码仅表示单次请求结果；对于一个步骤多个请求的综合响应结果，需要使用其它方式表示。
    """

    # 通用错误码

    CONTINUE = 2, '继续'
    """继续。表示本次请求已经执行完毕，但需要继续轮询，直至完成、成功，或响应错误代码。"""

    SUCCEED = 1, '成功'
    """成功。表示本次请求已经执行完毕，并且 I/O 执行无误。"""

    DONE = 0, '完成'
    """完成。表示本次请求已经执行完毕。"""

    FAILED = -1, '失败'
    """失败。表示本次请求因不可预料或未能预料的原因中断执行。当没有敲定错误码时，也可以使用该错误码临时代替。"""

    # TODO: 以下错误码仅限参考，请根据项目实际需求增补、改编或重构。目前错误码暂未超出 16 位有符号整数的存储空间。

    # 客户端侧错误
    MISSING_PARAMS = -4001, '缺少参数'
    INVALID_PARAMS = -4002, '提供了错误的参数值或参数类型'
    INVALID_CERTIFICATE = -4003, '鉴权凭证不合法'
    RESOURCE_NOT_FOUND = -4004, '资源未找到'

    # 服务端侧错误
    INTERNAL_ERROR = -5000, '服务器内部未知错误'
    NOT_IMPLEMENTED = -5001, '接口未实现'
    DEPENDENCE_ERROR = -5002, '上游服务返回错误响应'
    DEPENDENCE_UNAVAILABLE = -5003, '上游服务不可用'
    DEPENDENCE_TIMEOUT = -5004, '上游服务响应超时'

    # 授权鉴权服务侧错误
    FAIL_AUTHORIZE = -7001, '授权失败'
    FAIL_OBTAIN_OPENID = -7002, 'OpenID 获取失败'
    FAIL_EXCHANGE_TOKEN = -7003, '访问令牌交换失败'
    FAIL_OBTAIN_PROFILES = -7004, '用户资料获取失败'
    FAIL_LOGOUT = -7005, '登出失败'
    AUTHENTICATION_UNSUPPORTED = -7006, '认证方式不受支持'
    AUTHORIZATION_TERMINATED = -7007, '授权流程被终止'
    WRONG_ACCOUNT_TYPE = -7008, '账号类型错误（不是一个用户）'
    APP_NOT_FOUND = -7009, 'OAuth 应用不存在'

    @property
    def ok(self) -> bool:
        """
        错误码是否在“正常”范围？
        """
        return self >= Errcode.DONE


class _ErrcodeScope:

    def __new__(cls, *args, **kwargs):
        return Errcode(*args, **kwargs)


class _Client(_ErrcodeScope):
    MISSING_PARAMS = Errcode.MISSING_PARAMS
    INVALID_PARAMS = Errcode.INVALID_PARAMS
    INVALID_CERTIFICATE = Errcode.INVALID_CERTIFICATE
    RESOURCE_NOT_FOUND = Errcode.RESOURCE_NOT_FOUND


class _Server(_ErrcodeScope):
    INTERNAL_ERROR = Errcode.INTERNAL_ERROR
    NOT_IMPLEMENTED = Errcode.NOT_IMPLEMENTED
    DEPENDENCE_ERROR = Errcode.DEPENDENCE_ERROR
    DEPENDENCE_UNAVAILABLE = Errcode.DEPENDENCE_UNAVAILABLE
    DEPENDENCE_TIMEOUT = Errcode.DEPENDENCE_TIMEOUT


class _Auth(_ErrcodeScope):
    FAIL_AUTHORIZE = Errcode.FAIL_AUTHORIZE
    FAIL_OBTAIN_OPENID = Errcode.FAIL_OBTAIN_OPENID
    FAIL_EXCHANGE_TOKEN = Errcode.FAIL_EXCHANGE_TOKEN
    FAIL_OBTAIN_PROFILES = Errcode.FAIL_OBTAIN_PROFILES
    FAIL_LOGOUT = Errcode.FAIL_LOGOUT
    AUTHENTICATION_UNSUPPORTED = Errcode.AUTHENTICATION_UNSUPPORTED
    AUTHORIZATION_TERMINATED = Errcode.AUTHORIZATION_TERMINATED
    WRONG_ACCOUNT_TYPE = Errcode.WRONG_ACCOUNT_TYPE
    APP_NOT_FOUND = Errcode.APP_NOT_FOUND


Errcode.Client = _Client
"""客户端侧错误。"""

Errcode.Server = _Server
"""服务端侧错误。"""

Errcode.Auth = _Auth
"""授权鉴权服务侧错误。"""


def _standardize(data: Any = None, code: Errcode = Errcode.FAILED, msg: str = None, **kwargs: Any) -> dict:
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
    if 'context' in body and body['context'] is None:
        _ = body.pop('context')

    assert 'data' in body, 'API响应缺少 "data" 字段。'
    assert 'code' in body, 'API响应缺少 "code" 字段。'
    assert 'message' in body, 'API响应缺少 "message" 字段。'
    assert type(body['code']) is int, 'API响应的 "code" 字段必须是 int 类型。'
    assert type(body['message']) is str, 'API响应的 "message" 字段必须是 str 类型。'
    assert body['message'], 'API响应的 "message" 字段不允许为空字符串。'
    if 'pages' in body:
        assert type(body['pages']) is int, 'API响应的 "pages" 字段必须是 int 类型。'
    return body


def resp200(data: Any = None, code: Errcode = Errcode.FAILED, msg: str = None, **kwargs: Any) -> Response:
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
    - ``context`` 表示上下文信息，一般用于反馈给开发人员定位问题。可以是任意类型，但若为 ``null`` 则会在标准化过程中移除该字段。
      多数情况下是 Django REST Framework 序列化器校验时抛出的异常信息，类型为嵌套数组或嵌套对象。

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
    :param code: 封装过程中手动指定的错误码。如果响应未被封装，则错误码与该参数未必相同。
    :return: 符合标准格式的响应。
    """
    if not isinstance(response.data, dict) or len({'code', 'message', 'data'} - set(response.data.keys())) > 0:
        response.data = _standardize(response.data, code=code)

    return response


if __name__ == '__main__':
    assert Errcode.NOT_IMPLEMENTED is Errcode.Server.NOT_IMPLEMENTED
    assert (
            Errcode.NOT_IMPLEMENTED.value
            == Errcode.NOT_IMPLEMENTED
            == Errcode(Errcode.NOT_IMPLEMENTED.value)
            == Errcode.Server.NOT_IMPLEMENTED
            == Errcode.Server(Errcode.NOT_IMPLEMENTED.value)
    )
