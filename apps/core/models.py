from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models

from utils.models import SnakeModel


class MemberManger(UserManager):
    """
    系统用户管理器。

    这个管理器的默认查询集会剔除已注销用户（is_active=False）。
    """

    def get_queryset(self):
        return super().get_queryset().filter(is_active=True)


class User(AbstractUser, metaclass=SnakeModel):
    """
    系统用户。
    """
    username = models.CharField('用户名', max_length=50, unique=True, validators=[AbstractUser.username_validator])
    nickname = models.CharField('昵称', max_length=100, null=True, default=None)

    objects = UserManager()
    members = MemberManger()

    class Meta:
        verbose_name = '用户'
        verbose_name_plural = '用户'
