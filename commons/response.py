__all__ = [
    'Errcode',
    'resp200',
    'standardize',
]

from typing import Any

from django.db.models import IntegerChoices
from rest_framework.response import Response


# TODO: 以下错误码仅限参考，请根据项目实际需求增补、改编或重构。目前错误码暂未超出 16 位有符号整数的存储空间。
class Errcode(IntegerChoices):
    """
    错误码。

    - 项目 API 响应状态码，出现在 HTTP 响应数据内，主要用于前端、调用端识别 API 响应状态。
    - 单个错误码仅表示单次请求结果；对于一个步骤多个请求的综合响应结果，需要使用其它方式表示。
    """

    CONTINUE = 2, '继续'
    """表示本次请求已经执行完毕，但需要继续轮询，直至完成、成功，或响应错误代码。"""

    DONE = 0, '完成'
    """表示本次请求已经执行完毕。"""

    FAILED = -1, '失败'
    """表示本次请求因不可预料或未能预料的原因中断执行。当没有敲定错误码时，也可以使用该错误码临时代替。"""

    INVALID_REQUEST = -4000, '请求内容解析失败'
    MISSING_PARAMS = -4001, '缺少参数'
    INVALID_PARAMS = -4002, '提供了错误的参数值或参数类型'
    INVALID_CERTIFICATE = -4003, '鉴权凭证不合法'
    RESOURCE_NOT_FOUND = -4004, '资源未找到'

    INTERNAL_ERROR = -5000, '服务器内部未知错误'
    NOT_IMPLEMENTED = -5001, '接口未实现'
    DEPENDENCE_ERROR = -5002, '上游服务返回错误响应'
    DEPENDENCE_UNAVAILABLE = -5003, '上游服务不可用'
    DEPENDENCE_TIMEOUT = -5004, '上游服务响应超时'

    @property
    def ok(self) -> bool:
        """
        错误码是否在“正常”范围？
        """
        return self >= Errcode.DONE

    # 该方法可能会被高频使用，因此简写参数名。
    def __call__(self, msg: str = None, ctx: Any = None, data=None, **fields) -> Response:
        """
        构造基于 :class:`Errcode` 的标准格式的响应。

        :param msg: 错误提示。默认为当前枚举的提示。
        :param ctx: 上下文信息。若为 ``None`` 则不会出现在响应报文中。
        :param data: 业务数据，默认为空。
        :param fields: 其它需要加入到响应报文的字段，不能含有 ``errcode``、``message`` 与 ``context`` 三个字段。
        :return: Django REST Framework 响应对象 :class:`Response` 。
        """
        assert 'errcode' not in fields, f'{self!r}() 不能接受名为 errcode 的额外参数，请改用 code= 传递，或重命名。'
        assert 'message' not in fields, f'{self!r}() 不能接受名为 message 的额外参数，请改用 msg= 传递，或重命名。'
        assert 'context' not in fields, f'{self!r}() 不能接受名为 context 的额外参数，请改用 ctx= 传递，或重命名。'
        assert not self.ok, f'请使用 {resp200.__name__}(code={self!r}) 代替 {self!r}() 构造响应对象。'
        body = _standardize(data, errcode=self, message=msg, context=ctx, **fields)
        return Response(body)


def _standardize(
        data: Any,
        errcode: Errcode,
        message: str = None,
        context: Any = None,
        **fields: Any,
) -> dict:
    """
    构造标准的响应格式。

    :param errcode: 错误代码。
    :param message: 错误提示。不提供则默认为 ``errcode`` 对应的提示。
    :param context: 上下文。若为 ``None`` 则不会出现在响应报文中。
    :param data: 要返回的业务数据部分。
    :param fields: 其它需要加入到响应报文的字段。
    :return: 一个字典。
    """
    body = {
        'errcode': errcode.value,
        'message': message or errcode.label,
        'context': context,
        'data': data,
        **fields,
    }
    if body['context'] is None:
        body.pop('context')

    assert 'data' in body, 'API 响应缺少 "data" 字段。'
    assert 'errcode' in body, 'API 响应缺少 "errcode" 字段。'
    assert 'message' in body, 'API 响应缺少 "message" 字段。'
    assert type(body['errcode']) is int, 'API 响应的 "errcode" 字段必须是 int 类型。'
    assert type(body['message']) is str, 'API 响应的 "message" 字段必须是 str 类型。'
    assert body['message'], 'API 响应的 "message" 字段不允许为空字符串。'
    if 'context' in body:
        assert body['context'] is not None, '"context" 字段为空时不应出现在 API 响应中。'
    if 'pages' in body:
        assert type(body['pages']) is int, 'API 响应的 "pages" 字段必须是 int 类型。'
    return body


# 该函数可能会被高频使用，因此简写参数名。
def resp200(
        data: Any = None,
        *,
        code: Errcode = Errcode.DONE,
        msg: str = None,
        ctx: Any = None,
        **fields: Any,
) -> Response:
    """
    构造具有标准格式的响应。

    标准响应的 HTTP 响应状态码固定为
    `200 OK <https://developer.mozilla.org/zh-CN/docs/Web/HTTP/Status/200>`_，报文内容为一段包含以下字段的
    JSON：（必定存在 ``errcode``、``message``、``context`` 三个字段）

    - ``errcode`` 表示错误代码，必定存在，必定为 integer（int32）。参见 :class:`Errcode` 。
    - ``message`` 表示错误提示，必定存在，必定为 string 且不为空字符串，不应存在换行符，不建议以句号结尾。
    - ``context`` 表示上下文信息，一般用于反馈给开发人员定位问题。可以是任意类型，但若为 ``null`` 则会从响应中移除该字段。
      多数情况下是 Django REST Framework 序列化器校验时抛出的异常信息，类型为嵌套数组或嵌套对象。
    - ``data`` 表示业务数据，必定存在，且可以为 ``null`` 或其它任意类型。
    - ``prev`` 表示上一页的单个请求 URL，可以为 string 或 ``null``，不能是空字符串。
    - ``next`` 表示下一页的单个请求 URL，可以为 string 或 ``null``，不能是空字符串。
    - ``pages`` 表示总页数，必定为 integer（int64）。

    :param data: 要返回的业务数据部分，默认为空。
    :param code: 错误代码，默认为完毕。
    :param msg: 错误提示。不提供则默认为 ``code`` 的标签。
    :param ctx: 上下文信息。若为 ``None`` 则不会出现在响应报文中。
    :param fields: 其它需要加入到响应报文的字段，不能含有 ``errcode``，``message`` 与 ``context`` 三个字段。
    :return: Django REST Framework 响应对象 :class:`Response` 。
    """
    assert 'errcode' not in fields, f'{resp200.__name__}() 不能接受名为 errcode 的额外参数，请改用 code= 传递，或重命名。'
    assert 'message' not in fields, f'{resp200.__name__}() 不能接受名为 message 的额外参数，请改用 msg= 传递，或重命名。'
    assert 'context' not in fields, f'{resp200.__name__}() 不能接受名为 context 的额外参数，请改用 ctx= 传递，或重命名。'
    body = _standardize(data, errcode=code, message=msg, context=ctx, **fields)
    return Response(body)


def standardize(response: Response, *, errcode: Errcode) -> Response:
    """
    如果 **响应内容** 不符合标准格式，则封装为标准格式。

    :param response: 原始响应。
    :param errcode: 封装过程中手动指定的错误码。如果响应未被封装，则错误码与该参数未必相同。
    :return: 符合标准格式的响应。
    """
    if not isinstance(response.data, dict) or len({'errcode', 'message', 'data'} - set(response.data.keys())) > 0:
        response.data = _standardize(response.data, errcode=errcode)

    return response
