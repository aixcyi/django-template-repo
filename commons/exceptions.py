__all__ = [
    'MeowViewException',
]

from commons.response import Errcode, resp200


class MeowViewException(Exception):

    # 该方法可能会被高频使用，因此简写参数名。
    def __init__(self, msg: str = None, *, ctx=None, code: Errcode = Errcode.FAILED, **kwargs):
        self.args = code, msg, ctx, kwargs
        self.errcode = code
        self.message = msg
        self.context = ctx
        self.fields = kwargs

    def as_response(self):
        return resp200(code=self.errcode, msg=self.message, ctx=self.context, **self.fields)
