"""
微信 API 接口。
"""

# TODO: 这既是微信 API 接口的简易封装，数量不多那么可堪一用；也是 ServiceRequest 的一个使用示例，快速对接功能不多的第二方服务接口。

import logging
from typing import Literal

from django.conf import settings
from django.db.models import IntegerChoices
from zeraora.string import StringBuilder

from commons.exceptions import MeowViewException
from utils.http import HTTPMethod
from utils.request import ServiceRequest

logger = logging.getLogger('project.api.wechat')


# TODO: 微信的 errcode 太多，只定义用得到的（比如要用来判断、要更友好的提示）就够了。
# https://developers.weixin.qq.com/doc/oplatform/Return_codes/Return_code_descriptions_new.html
class WeChatErrcode(IntegerChoices):
    EXCEED_API_RATE = 45011, '请求过快'
    LOGGING_BLOCKED = 40226, '用户无法登录'
    INVALID_CODE = 40029, 'code无效'
    SUCCEED = 0, '成功'
    FAILED = -1, '微信系统错误'


# noinspection PyPep8Naming
class WeChatRequest(ServiceRequest):
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

    def send(self):
        """
        执行请求，返回响应。

        - 详细记录请求细节与响应结果（发送到日志系统）。
        - 对底层 API 的错误处理。
        """
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
            code = int(body.pop('errcode', WeChatErrcode.SUCCEED))
            resp = WeChatResponse(
                __errcode__=code,
                errcode=WeChatErrcode(code) if code in WeChatErrcode else WeChatErrcode.FAILED,
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
        if resp.errcode < WeChatErrcode.SUCCEED:
            raise MeowViewException(msg=resp.errmsg, wxapi=resp.__errcode__, **resp.fields())
        return resp

    @classmethod
    def post(cls, api: str, **kwargs):
        resp = cls('POST', api, **kwargs).send()
        if resp.errcode < WeChatErrcode.SUCCEED:
            raise MeowViewException(msg=resp.errmsg, wxapi=resp.__errcode__, **resp.fields())
        return resp

    @classmethod
    def code2session(cls, js_code: str, appid: str | None = None, secret: str | None = None):
        """
        微信
        `code2session <https://developers.weixin.qq.com/miniprogram/dev/OpenApiDoc/user-login/code2Session.html>`_
        """
        return cls.get(
            '/sns/jscode2session',
            params={
                'appid': appid or settings.WECHAT_APP_ID,
                'secret': secret or settings.WECHAT_APP_SECRET,
                'js_code': js_code,
                'grant_type': 'authorization_code',
            },
        )

    @classmethod
    def getAccessToken(cls, appid: str | None = None, secret: str | None = None):
        """
        微信
        `getAccessToken <https://developers.weixin.qq.com/miniprogram/dev/server/API/mp-access-token/api_getaccesstoken.html>`_
        """
        return cls.get(
            '/cgi-bin/token',
            params={
                'appid': appid or settings.WECHAT_APP_ID,
                'secret': secret or settings.WECHAT_APP_SECRET,
                'grant_type': 'client_credential',
            },
        )


class WeChatResponse:
    STANDARD_FIELDS = 'errcode', 'errmsg'

    __errcode__: int
    errcode: WeChatErrcode
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

    # TODO: 缺少某个字段时返回 None 而不是抛出 AttributeError。
    def __getattr__(self, item):
        return None

    def fields(self, with_standard_fields=False) -> dict:
        if with_standard_fields:
            return self.__dict__.copy()
        return {
            attr: self.__dict__[attr]
            for attr in self.__dict__
            if attr not in self.STANDARD_FIELDS and not attr.startswith('__')
        }
