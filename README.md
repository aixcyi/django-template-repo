# django template repo

Django 4.2 项目的模板仓库。

## 优点

- 可以隔离不同环境的配置。
- 更加易读的 settings.py 。
- 生成更易读的表名，比如 `order.models.GoodsSKUInfo` 会创建 `order_goods_sku_info` 表，而不会是 `order_goodsskuinfo` 。
- 自带 alarms.log、records.log、requests.log 三个日志配置。
- 自定义 `User` 模型（放在自带的 `core` app里）。
- 将 Django App 集中存放在 ./apps 目录下。

## 用法

> [我应该使用哪个版本的 Python 来配合 Django？](https://docs.djangoproject.com/zh-hans/4.2/faq/install/#what-python-version-can-i-use-with-django)

1. [从模板创建仓库 - GitHub](https://docs.github.com/zh/repositories/creating-and-managing-repositories/creating-a-repository-from-a-template) ；
2. 克隆刚刚创建的仓库；
3. 使用 IDE 打开项目，将文件夹 ./django_template_repo 重命名为你的项目名，同时，连带重命名 **所有** 相关引用和字符串；
4. 根据需要创建虚拟环境，并切换到虚拟环境中；
5. 在 ./django_template_repo 中创建自己的配置文件 settings_dev.py ；
6. 将以下文件里的环境变量 `DJANGO_SETTINGS_MODULE` 的值修改为 `"django_template_repo.settings_dev"` ；
   - ./manage.py
   - ./django_template_repo/asgi.py
   - ./django_template_repo/wsgi.py
7. `python manage.py runserver` 运行项目。

### 配置设置

> - [Django Settings 快速配置](https://docs.djangoproject.com/zh-hans/4.2/topics/settings/)
> - [Django Settings 完整配置列表](https://docs.djangoproject.com/zh-hans/4.2/ref/settings/)
> - [Django REST Framework Settings](https://www.django-rest-framework.org/api-guide/settings/)

./django_template_repo/settings_*.py 不会被纳入版本管理，
你可以通过创建不同命名的配置来实现生产环境和开发环境的隔离，
比如用 `settings_dev.py` 配置开发环境，用 `settings_prod.py` 来配置生产环境。

仅 `SECRET_KEY` 是必须进行配置的。
使用以下代码可以快速生成十个随机 `SECRET_KEY` 备选：

```python
from base64 import b85encode
from random import getrandbits

for _ in range(10):
    soup = getrandbits(64 * 8).to_bytes(64, 'big')
    key = b85encode(soup).decode('ASCII')
    print(key)
```

### 创建 App

可以通过 PyCharm 插件 [Tiny Snake](https://plugins.jetbrains.com/plugin/24140-tiny-snake/)
快速创建带有 `serializers.py` 和 `urls.py` 的 App 。

亦或者通过 django-admin 命令在 ./apps 内创建，参数与
[`startapp`](https://docs.djangoproject.com/zh-hans/4.2/ref/django-admin/#startapp)
相近，并且可以分别通过指定 `-s` 和 `-u` 标志来创建 `serializers.py` 和 `urls.py` 。

```shell
python manage.py newapp APPNAME -su
```

## 配置模板

### settings_dev.py

适用于本地调试环境。

```python
from django_template_repo.settings import *

DEBUG = True
SECRET_KEY = '<随机生成的任意ASCII字符>'
ALLOWED_HOSTS = [
   '*',
]

# 确保目录一定存在
LOGS_DIR.mkdir(exist_ok=True)  # 日志目录
MEDIA_ROOT.mkdir(exist_ok=True)  # 用户上传目录
STATIC_ROOT.mkdir(exist_ok=True)  # 静态文件目录
```

### settings_prod.py

适用于生产环境。

```python
from django_template_repo.settings import *

SECRET_KEY = '<随机生成的任意ASCII字符>'

# 确保目录一定存在
LOGS_DIR.mkdir(exist_ok=True)  # 日志目录
```

### PostgreSQL 配置模板

[注意事项](https://docs.djangoproject.com/zh-hans/4.2/ref/databases/#postgresql-notes)

```python
DATABASES = {
    'default': dict(
        ENGINE='django.db.backends.postgresql',
        NAME='<数据库名称>',
        USER='postgres',
        PASSWORD='<账号密码>',
        HOST='127.0.0.1',
        PORT='5432',
    ),
}
```

### MySQL 配置模板

[注意事项](https://docs.djangoproject.com/zh-hans/4.2/ref/databases/#mysql-notes)

```python
DATABASES = {
    'default': dict(
        ENGINE='django.db.backends.mysql',
        NAME='<数据库名称>',
        USER='root',
        PASSWORD='<账号密码>',
        HOST='127.0.0.1',
        PORT='3306',
    ),
}
```

### Oracle 配置模板

[注意事项](https://docs.djangoproject.com/zh-hans/4.2/ref/databases/#oracle-notes)

```python
DATABASES = {
    'default': dict(
        ENGINE='django.db.backends.oracle',
        NAME='<数据库名称>',
        USER='system',
        PASSWORD='<账号密码>',
        HOST='127.0.0.1',
        PORT='1521',
    ),
}
```

### SQLite 配置模板

[注意事项](https://docs.djangoproject.com/zh-hans/4.2/ref/databases/#sqlite-notes)

```python
from django_template_repo.settings import BASE_DIR

DATABASES = {
    'default': dict(
        ENGINE='django.db.backends.sqlite3',
        NAME=BASE_DIR / '数据库名称.sqlite3',
    ),
}
```

### Redis 配置模板

[设置缓存](https://docs.djangoproject.com/zh-hans/4.2/topics/cache/#redis)

```python
CACHES = {
    'default': dict(
        BACKEND='django.core.cache.backends.redis.RedisCache',
        LOCATION='redis://127.0.0.1:6379/0',
    ),
}
```
