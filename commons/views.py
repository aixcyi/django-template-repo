__all__ = [
    'SoftDeleteModelMixin',
    'MeowAPIView',
    'MeowViewSet',
    'MeowModelViewSet',
]

# TODO: Python 3.11 新增，请按照实际依赖进行修改。
from http import HTTPMethod

from django.db import IntegrityError
from rest_framework import mixins, status
from rest_framework.exceptions import APIException
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import SAFE_METHODS
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

from commons.exceptions import MeowViewException
from commons.response import Errcode, resp200, wrap200
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
                '模型 %s 没有用于标记删除的字段 %s 。' % (
                    type(instance).__name__,
                    self.deletion_field,
                )
            )

        setattr(instance, self.deletion_field, self.deletion_mark)

        instance.save()


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
            return resp200(msg=str(exc))

        # Django REST Framework 异常根类
        if isinstance(exc, APIException):
            if isinstance(exc.detail, str):
                return resp200(msg=str(exc.detail))
            else:
                return resp200(msg=str(exc.default_detail), context=exc.detail)

        # 项目自定义的异常根类
        if isinstance(exc, MeowViewException):
            return exc.as_response()

        return super().handle_exception(exc)


class MeowViewSet(EasyViewSetMixin,
                  MeowAPIView,
                  GenericAPIView):
    """
    此类是对基于API接口集合的视图类（GenericAPIView+ViewSetMixin）的定制。
    """
    pass


class MeowModelViewSet(mixins.CreateModelMixin,
                       mixins.ListModelMixin,
                       mixins.RetrieveModelMixin,
                       mixins.UpdateModelMixin,
                       SoftDeleteModelMixin,
                       MeowViewSet):

    def finalize_response(self, request, response: Response, *args, **kwargs):
        old = super().finalize_response(request, response, *args, **kwargs)

        # TODO: Python 3.11 以前将判断 method 的逻辑改为直接判断 'GET', 'POST' 等字符串。
        method = HTTPMethod(request.method)

        if method == HTTPMethod.OPTIONS:
            return old

        if response.content_type == JSONRenderer.media_type or response.content_type is None:
            if response.status_code // 100 != 2:
                code = Errcode.FAILED
            elif method == HTTPMethod.GET:
                code = Errcode.DONE
            else:
                code = Errcode.SUCCEED

            response = wrap200(response, code=code)

        return response
