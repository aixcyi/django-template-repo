from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models

from utils.models import SnakeModel


class ActiveUserManger(UserManager):
    """
    未注销用户管理器。

    这个管理器的 **默认查询集** 会通过 ``is_active=False`` 排除已注销用户。
    """

    def get_queryset(self):
        return super().get_queryset().filter(is_active=True)


class User(AbstractUser, metaclass=SnakeModel):
    """
    用户。
    """
    id = models.BigAutoField('ID', primary_key=True)
    username = models.CharField('用户名', max_length=50, unique=True, validators=[AbstractUser.username_validator])
    nickname = models.CharField('昵称', max_length=100, null=True, default=None)

    objects = UserManager()
    users = ActiveUserManger()

    class Meta:
        verbose_name = '用户'
        verbose_name_plural = '用户'
