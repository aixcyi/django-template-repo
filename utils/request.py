from abc import ABC, abstractmethod
from typing import Literal

import requests
from django.http import QueryDict
from django.views import View

from utils.http import HTTPMethod


class ServiceRequest(ABC):
    """
    通用请求对象。
    """

    endpoint: str = ''
    """API 地址根部，不应以 ``/`` 结尾。"""

    @property
    def url(self) -> str:
        if not self.query:
            return f'{self.endpoint}{self.path}'
        return f'{self.endpoint}{self.path}?{self.query.urlencode()}'

    def __init__(
        self,
        method: HTTPMethod | Literal['CONNECT', 'DELETE', 'GET', 'HEAD', 'OPTIONS', 'PATCH', 'POST', 'PUT', 'TRACE'],
        path: str,
        **kwargs,
    ):
        assert method.lower() in View.http_method_names
        assert path.startswith('/')
        assert not self.endpoint.endswith('/')
        match method:
            case 'CONNECT' | 'DELETE' | 'GET' | 'HEAD' | 'OPTIONS' | 'PATCH' | 'POST' | 'PUT' | 'TRACE':
                self.method = method
            case HTTPMethod():
                self.method = str(method.name)
            case _:
                raise ValueError('HTTP 方法必须是一个字面量或枚举。')
        self.method: Literal['CONNECT', 'DELETE', 'GET', 'HEAD', 'OPTIONS', 'PATCH', 'POST', 'PUT', 'TRACE']
        self.path = path
        self.headers = kwargs.pop('headers', {}) or {}
        self.query = self._standardize(kwargs.pop('params', {}))
        self.data = dict(kwargs.get('data', {}))  # 传递给底层推断 Accept 头
        self.data.update(kwargs.get('json', {}))
        self.kwargs = kwargs

    @abstractmethod
    def send(self):
        raise NotImplementedError

    def _request(self) -> requests.Response:
        return requests.request(self.method, self.url, headers=self.headers, **self.kwargs)

    @classmethod
    def _query_from_dict(cls, params: dict, base: QueryDict | None = None) -> QueryDict:
        query = base or QueryDict(mutable=True)
        for k, v in params.items():
            match v:
                case list():
                    query.setlist(k, query.getlist(k) + v)
                case tuple() | set():
                    query.setlist(k, query.getlist(k) + list(v))
                case _:
                    query[k] = v
        return query

    @classmethod
    def _standardize(cls, params: str | dict | QueryDict | None = None, **kwargs) -> QueryDict:
        match params:
            case None:
                query = QueryDict('', mutable=True)
            case QueryDict():
                query = params.copy()
            case dict():
                query = cls._query_from_dict(params)
            case str():
                query = QueryDict(params, mutable=True)
            case _:
                raise ValueError(f'不接受 {type(params).__name__} 类型的 URL Query 。')

        query = cls._query_from_dict(kwargs, base=query)
        return query

    @classmethod
    @abstractmethod
    def get(cls, api: str, **kwargs):
        raise NotImplementedError

    @classmethod
    @abstractmethod
    def post(cls, api: str, **kwargs):
        raise NotImplementedError
