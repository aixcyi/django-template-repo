__all__ = [
    'SystemUserManger',
    'User',
    'WechatUser',
]

from random import choices

from django.contrib.auth.models import AbstractUser, Group, Permission, UserManager
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models
from django.utils import timezone
from zeraora.django import PrefilterManager, SnakeModel
from zeraora.string import Notation
from zeraora.uuid import uuid7


class SystemUserManger(UserManager):

    def get_queryset(self):
        return super().get_queryset().filter(is_active=True)

    def create_user(self, username=None, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(username or User.generate_username(), email, password, **extra_fields)

    async def acreate_user(self, username=None, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return await self._acreate_user(username or User.generate_username(), email, password, **extra_fields)


class User(AbstractUser, metaclass=SnakeModel):
    """
    系统用户。
    """

    # 验证器
    username_validator = UnicodeUsernameValidator()

    # 标识符／认证字段
    id = models.BigAutoField('ID', primary_key=True)
    uid = models.UUIDField('用户唯一ID', unique=True, default=uuid7, editable=False)
    username = models.CharField('用户名', max_length=50, unique=True, validators=[username_validator])
    password = models.CharField('密码', max_length=128)
    email = models.EmailField('电子邮箱', blank=True)

    # 鉴权字段
    is_superuser = models.BooleanField('是超级管理员', default=False, help_text='指无须显式分配即可拥有所有权限')
    is_staff = models.BooleanField('是管理员', default=False, help_text='用户是否可以登录管理站点。')
    is_active = models.BooleanField('未注销', default=True, help_text='用标记删除取代物理删除。')
    groups = models.ManyToManyField(
        Group,
        verbose_name='用户组',
        blank=True,
        help_text='用户自动获得每个组的所有权限。',
        related_name='user_set',
        related_query_name='user',
    )
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name='权限集',
        blank=True,
        help_text='用户拥有的所有权限。',
        related_name='user_set',
        related_query_name='user',
    )

    # 记录字段
    date_joined = models.DateTimeField('注册时间', default=timezone.now)
    last_login = models.DateTimeField('最后登录时间', blank=True, null=True)

    # 信息字段
    first_name = models.CharField('名称', max_length=150, blank=True)
    last_name = models.CharField('姓氏', max_length=150, blank=True)
    nickname = models.CharField('昵称', max_length=100, blank=True)

    # 管理器
    objects = SystemUserManger()
    members = PrefilterManager(is_active=True)

    class Meta:
        verbose_name = '用户'
        verbose_name_plural = '用户'

    @classmethod
    def generate_username(cls):
        """
        生成一个随机的用户名用作默认值。
        """
        # TODO: 在这里自定义不同项目的默认用户名。
        return 'fox' + ''.join(choices(list(Notation.BASE62), k=11))

    @property
    def seed(self) -> int:
        """
        每个用户独立的随机数种子。
        """
        # TODO: 如果不需要为每个用户配备独立的随机数种子，可以改为返回一个随机数，并考虑移除 uid 字段。
        return self.uid.int & 0x3FFF_FFFF_FFFF_FFFF

    def __str__(self):
        return self.nickname or self.username

    def get_username(self) -> str:
        return self.username


class WechatUser(models.Model, metaclass=SnakeModel):
    """
    微信小程序用户。
    """

    id = models.BigAutoField('ID', primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    openid = models.CharField('微信用户 OpenID', max_length=32, blank=True)
    unionid = models.CharField('微信用户 UnionID', max_length=32, blank=True)
    session = models.CharField('微信用户 Session Key', max_length=32, blank=True)

    objects = models.Manager()
    members = PrefilterManager(user__is_active=True)

    class Meta:
        verbose_name = '微信用户'
        verbose_name_plural = '微信用户'

    def __str__(self):
        return self.session
