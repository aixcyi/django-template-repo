"""
微信 API 接口。
"""

import logging
from typing import Literal

from django.conf import settings
from django.db.models import IntegerChoices
from zeraora.string import StringBuilder

from commons.exceptions import MeowViewException
from utils.http import HTTPMethod
from utils.request import ServiceRequest

logger = logging.getLogger('project.api.wechat')


# TODO: 按需增补状态码。
# https://developers.weixin.qq.com/doc/oplatform/Return_codes/Return_code_descriptions_new.html
class WechatErrcode(IntegerChoices):
    EXCEED_API_RATE = 45011, '请求过快'
    LOGGING_BLOCKED = 40226, '用户无法登录'
    INVALID_CODE = 40029, 'code无效'
    SUCCEED = 0, '成功'
    FAILED = -1, '微信系统错误'


class WechatRequest(ServiceRequest):
    """
    微信服务请求对象。
    """

    endpoint = 'https://api.weixin.qq.com'

    def __init__(
        self,
        method: HTTPMethod | Literal['CONNECT', 'DELETE', 'GET', 'HEAD', 'OPTIONS', 'PATCH', 'POST', 'PUT', 'TRACE'],
        path: str,
        **kwargs,
    ):
        super().__init__(method, path, **kwargs)
        self.headers.setdefault('Accept', 'application/json')

    # TODO: 按照喜好定制行为逻辑，包括但不限于删除或修改日志消息、改变响应数据的解析、异常处理……
    def send(self):
        try:
            logger.info(
                StringBuilder()
                .writeline(f'微信API：{self.method} {self.url}')
                .writes(f'{title}: {self.headers[title]}\n' for title in self.headers)
                .writes(f'{k} = {v}\n' for k, v in self.kwargs.items())
                .build()
            )
            response = self._request()
        except Exception as e:
            logger.exception(f'微信API：{self.method} {self.url} ERROR', exc_info=e)
            raise MeowViewException(msg='微信API不可用', http=False) from e
        if response.status_code // 100 != 2:
            raise MeowViewException(msg='微信API不可用', http=response.status_code)
        try:
            logger.info(
                StringBuilder()
                .writeline(f'微信API：{self.method} {self.url} {response.status_code}')
                .writeline(response.text)
                .build()
            )
            body = response.json()
            code = int(body.pop('errcode', WechatErrcode.SUCCEED))
            resp = WechatResponse(
                __errcode__=code,
                errcode=WechatErrcode(code) if code in WechatErrcode else WechatErrcode.FAILED,
                errmsg=str(body.pop('errmsg', '')),
                **body,
            )
        except Exception as e:
            logger.exception('微信API：响应格式有误', exc_info=e)
            raise MeowViewException(msg='微信API不可用', exc=type(e).__name__) from e
        return resp

    @classmethod
    def get(cls, api: str, **kwargs):
        resp = cls('GET', api, **kwargs).send()
        if resp.errcode < WechatErrcode.SUCCEED:
            raise MeowViewException(msg=resp.errmsg, wxapi=resp.__errcode__, **resp.fields())
        return resp

    @classmethod
    def post(cls, api: str, **kwargs):
        resp = cls('POST', api, **kwargs).send()
        if resp.errcode < WechatErrcode.SUCCEED:
            raise MeowViewException(msg=resp.errmsg, wxapi=resp.__errcode__, **resp.fields())
        return resp

    @classmethod
    def code2session(cls, js_code):
        """
        微信
        `code2session <https://developers.weixin.qq.com/miniprogram/dev/OpenApiDoc/user-login/code2Session.html>`_
        """
        return cls.get(
            '/sns/jscode2session',
            params={
                'appid': settings.WECHAT_APP_ID,
                'secret': settings.WECHAT_APP_SECRET,
                'js_code': js_code,
                'grant_type': 'authorization_code',
            },
        )


class WechatResponse:
    STANDARD_FIELDS = 'errcode', 'errmsg'

    __errcode__: int
    errcode: WechatErrcode
    errmsg: str

    def __init__(self, **attrs):
        inners = [self.fields.__name__]
        for func in inners:
            if func in attrs:
                attrs[f'{func}_'] = attrs.pop(func)
        self.__dict__.update(attrs)

    def __repr__(self):
        attrs = ','.join(f'{attr}={self.__dict__[attr]!s}' for attr in self.__dict__)
        return f'{self.__class__.__name__}({attrs})'

    def fields(self, with_standard_fields=False) -> dict:
        if with_standard_fields:
            return self.__dict__.copy()
        return {
            attr: self.__dict__[attr]
            for attr in self.__dict__
            if attr not in self.STANDARD_FIELDS and not attr.startswith('__')
        }
