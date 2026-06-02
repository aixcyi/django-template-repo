__all__ = [
    'SoftDeleteModelMixin',
    'MeowHandler',
    'MeowAPIView',
    'MeowViewSet',
    'MeowModelViewSet',
]

import sys
from contextlib import AbstractContextManager, ContextDecorator
from http import HTTPMethod
from inspect import currentframe

from django.core.exceptions import (
    ObjectDoesNotExist,
)
from django.core.exceptions import (
    ValidationError as DjangoValidationError,
)
from django.db import IntegrityError
from rest_framework import mixins, status
from rest_framework.exceptions import APIException
from rest_framework.exceptions import (
    ValidationError as RestValidationError,
)
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import SAFE_METHODS
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

from commons.exceptions import MeowViewException
from commons.response import Errcode, standardize
from utils.views import EasyViewSetMixin


class SoftDeleteModelMixin:
    """
    将一个模型实例标记为已删除。（软删除）

    - 通过 ``self.deletion_field`` 配置存储标记的字段，默认是 ``deleted``。
    - 通过 ``self.deletion_mark`` 配置标记是什么，默认是布尔值 ``True`` 。

    适用于：``rest_framework.generics.GenericAPIView`` 的子类
    """

    deletion_field = 'deleted'
    deletion_mark = True

    def soft_delete(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_soft_delete(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def perform_soft_delete(self, instance):
        if not hasattr(instance, self.deletion_field):
            raise TypeError(
                '模型 %s 没有用于标记删除的字段 %s 。'
                % (
                    type(instance).__name__,
                    self.deletion_field,
                )
            )

        setattr(instance, self.deletion_field, self.deletion_mark)

        instance.save()


# noinspection PyPep8Naming
class MeowHandler(ContextDecorator, AbstractContextManager):
    """
    将上下文内特定的异常转换成通用异常 :class:`MeowViewException` 。
    """

    def __init__(self):
        self._notfound: str | None = None
        self._skip_dj = False
        self._skip_drf = False

    def __exit__(self, klass: type[BaseException] | None, exc: BaseException | None, traceback):
        if klass is None or exc is None or traceback is None:
            return
        match exc:
            case KeyError():
                raise MeowViewException(msg=f'解析参数 {exc.args[0]} 不存在')
            case ValueError():
                raise MeowViewException(msg='参数解析失败')
            case TypeError():
                raise MeowViewException(msg='参数解析类型不一致')

            case ObjectDoesNotExist():
                if self._notfound is not None:
                    raise MeowViewException(msg=self._notfound)
                subclass = klass.mro()[0]
                model = getattr(sys.modules[subclass.__module__], subclass.__qualname__.split('.')[0])
                raise MeowViewException(msg=f'{model._meta.verbose_name} 不存在')

            case DjangoValidationError() if not self._skip_dj:
                major, *minors = exc.messages
                raise MeowViewException(msg=major, ctx=minors)

            case RestValidationError() if not self._skip_drf:
                if isinstance(exc.detail, str):
                    raise MeowViewException(msg=str(exc.detail))
                else:
                    raise MeowViewException(msg=str(exc.default_detail), ctx=exc.detail)

    def skipValidation(self, dj=True, drf=True):
        """
        忽略验证错误。

        :param dj: 是否忽略 Django 的验证错误。
        :param drf: 是否忽略 Django REST Framework 的验证错误。
        :return: 上下文管理器自身。
        """
        self._skip_dj = dj
        self._skip_drf = drf
        return self

    def catchNotfound(self, msg: str):
        """
        捕获并处理 :class:`ObjectDoesNotExist` 及其子类。

        :param msg: 响应的 ``message``，默认为对应 :class:`Errcode` 的提示。
        :return: 上下文管理器自身。
        """
        self._notfound = msg
        return self

    def typecheck(self, **types: type):
        """
        立刻检查上下文内的变量的类型。

        - 如果调用此方法，必须且只能在上下文内直接调用，否则会找不到变量。
        - 如果找不到指定的变量，将会触发 :class:`AssertionError` 。
        - 判定方式是 ``is``，不包含子类。
        - 该方法不会抛出异常。

        :param types: 参数名即变量名，参数值即类型。
        :return: 上下文管理器自身。
        """
        variables = currentframe().f_back.f_locals
        for name in types:
            assert name in variables, f'上下文内找不到变量 {name}'
            if type(variables[name]) is types[name]:
                continue
            raise MeowViewException(msg='参数解析类型不一致', ctx={'field': name})
        else:
            return self


class MeowAPIView(APIView):
    """
    此类是对基于API的视图类（APIView）的定制。
    """

    @property
    def safe(self) -> bool:
        """当前请求的请求方法是安全方法。"""
        return str(self.request.method).upper() in SAFE_METHODS

    @property
    def body(self):
        """请求体数据。"""
        return self.request.GET if self.safe else self.request.data

    def handle_exception(self, exc):
        """
        异常处理与响应封装。
        """
        # Django 捕获的来自数据库的异常
        if isinstance(exc, IntegrityError):
            return Errcode.FAILED(str(exc))

        # Django REST Framework 异常根类
        if isinstance(exc, APIException):
            if isinstance(exc.detail, str):
                return Errcode.FAILED(str(exc.detail))
            else:
                return Errcode.FAILED(str(exc.default_detail), ctx=exc.detail)

        # 项目自定义的异常根类
        if isinstance(exc, MeowViewException):
            return exc.as_response()

        return super().handle_exception(exc)


class MeowViewSet(EasyViewSetMixin, MeowAPIView, GenericAPIView):
    """
    此类是对基于API接口集合的视图类（GenericAPIView+ViewSetMixin）的定制。
    """

    pass


class MeowModelViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    SoftDeleteModelMixin,
    MeowViewSet,
):
    def finalize_response(self, request, response: Response, *args, **kwargs):
        old = super().finalize_response(request, response, *args, **kwargs)

        method = HTTPMethod(request.method)

        if method == HTTPMethod.OPTIONS:
            return old

        if response.content_type == JSONRenderer.media_type or response.content_type is None:
            if response.status_code // 100 != 2:
                errcode = Errcode.FAILED
            else:
                errcode = Errcode.DONE

            response = standardize(response, errcode=errcode)

        return response
