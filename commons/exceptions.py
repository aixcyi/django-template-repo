__all__ = [
    'MeowViewException',
]

from commons.response import Errcode, resp200


class MeowViewException(Exception):

    def __init__(self, msg: str = None, code: Errcode = Errcode.FAILED, **kwargs):
        self.args = code, msg, kwargs

    def as_response(self):
        return resp200(code=self.args[0], msg=self.args[1], **self.args[2])
