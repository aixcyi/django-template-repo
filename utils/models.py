__all__ = [
    'SnakeModel',
]

import re

from django.apps import apps
from django.db import models


class SnakeModel(models.base.ModelBase):
    """
    自动生成一个下划线小写的（蛇形）数据表名。

    >>> class YourModel(models.Model,
    >>>                 metaclass=SnakeModel):
    >>>     # 字段声明...
    >>>
    >>>     class Meta:
    >>>         # SnakeModel的生成格式
    >>>         db_table = "{app}_{snake_model_name}"
    >>>
    >>>         # Django的生成格式
    >>>         # db_table = "{app}_{lowermodelname}"

    - 不会覆盖已经指定了的表名。
    - 可以用于抽象模型中，但只会为继承了抽象模型的非抽象模型生成表名。

    适用于：``django.db.models.Model`` 的子类
    """

    def __new__(cls, name, bases, attrs, **kwargs):
        module = attrs.get('__module__', None)
        app_config = apps.get_containing_app_config(module)
        if app_config is None:
            return super().__new__(cls, name, bases, attrs, **kwargs)

        app_name = app_config.label

        model_name = re.sub(r'[A-Z]', (lambda s: f'_{s.group(0).lower()}'), name)
        model_name = model_name[1:] if model_name.startswith('_') else model_name

        table_name = f'{app_name}_{model_name}'

        if 'Meta' not in attrs:
            attrs['Meta'] = type('Meta', (), dict(db_table=table_name))

        abstract = getattr(attrs["Meta"], 'abstract', False)
        if not hasattr(attrs["Meta"], 'db_table') and not abstract:
            setattr(attrs['Meta'], 'db_table', table_name)

        return super().__new__(cls, name, bases, attrs, **kwargs)
