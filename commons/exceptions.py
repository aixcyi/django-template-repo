__all__ = [
    'MeowViewException',
    'APINotImplemented',
]

from rest_framework import status

from commons.response import Errcode, resp200


class MeowViewException(Exception):
    """
    项目根异常。

    该异常一般从业务层／视图层抛出，用于阻断业务／视图的继续执行，并返回一个前端可识别的报文。
    """

    tip: str | None = None
    """默认的错误提示。"""

    status: int = status.HTTP_200_OK
    """默认的 HTTP 响应状态码。"""

    # 该方法可能会被高频使用，因此简写参数名。
    def __init__(self, msg: str | None = tip, *, ctx=None, code: Errcode = Errcode.FAILED, **fields):
        """
        :param msg: 错误提示。不提供则默认为 ``code`` 的标签。
        :param ctx: 上下文信息。若为 ``None`` 则不会出现在响应报文中。
        :param code: 错误代码，默认为失败。
        :param fields: 其它需要加入到响应报文的字段，不能含有 ``errcode``，``message`` 与 ``context`` 三个字段。
        """
        assert 'errcode' not in fields, f'{self.__class__.__name__}() 不接受名为 errcode 的参数，请改用 code= 传递。'
        assert 'message' not in fields, f'{self.__class__.__name__}() 不接受名为 message 的参数，请改用 msg= 传递。'
        assert 'context' not in fields, f'{self.__class__.__name__}() 不接受名为 context 的参数，请改用 ctx= 传递。'
        self.args = code, msg, ctx, fields
        self.errcode = code
        self.message = msg
        self.context = ctx
        self.fields = fields

    def as_response(self):
        r = resp200(code=self.errcode, msg=self.message, ctx=self.context, **self.fields)
        r.status_code = self.status
        return r


class APINotImplemented(MeowViewException):
    """
    接口未被实现。
    """

    tip = '接口未实现'
    status = status.HTTP_501_NOT_IMPLEMENTED
