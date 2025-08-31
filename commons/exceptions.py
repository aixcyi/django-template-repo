__all__ = [
    'MeowViewException',
]

from commons.response import Errcode, resp200


class MeowViewException(Exception):

    # 该方法可能会被高频使用，因此简写参数名。
    def __init__(self, msg: str = None, *, ctx=None, code: Errcode = Errcode.FAILED, **fields):
        """
        项目根异常。

        该异常一般从业务层／视图层抛出。

        :param msg: 错误提示。不提供则默认为 ``code`` 的标签。
        :param ctx: 上下文信息。若为 ``None`` 则不会出现在响应报文中。
        :param code: 错误代码，默认为失败。
        :param fields: 其它需要加入到响应报文的字段，不能含有 ``errcode``，``message`` 与 ``context`` 三个字段。
        """
        assert 'errcode' not in fields, f'{self.__class__.__name__}() 不能接受名为 errcode 的额外参数，请改用 code= 传递，或重命名。'
        assert 'message' not in fields, f'{self.__class__.__name__}() 不能接受名为 message 的额外参数，请改用 msg= 传递，或重命名。'
        assert 'context' not in fields, f'{self.__class__.__name__}() 不能接受名为 context 的额外参数，请改用 ctx= 传递，或重命名。'
        self.args = code, msg, ctx, fields
        self.errcode = code
        self.message = msg
        self.context = ctx
        self.fields = fields

    def as_response(self):
        return resp200(code=self.errcode, msg=self.message, ctx=self.context, **self.fields)
