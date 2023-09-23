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

> 参见 [Django Settings](https://docs.djangoproject.com/zh-hans/4.2/ref/settings/)、[Django REST Framework Settings](https://www.django-rest-framework.org/api-guide/settings/)

./django_template_repo/settings_*.py 不会被纳入版本管理，你可以通过创建不同命名的配置来实现生产环境和开发环境的隔离，比如用 `settings_dev.py` 配置开发环境，用 `settings_prod.py` 来配置生产环境。

```python
from django_template_repo.settings import *

# ---------------- 以下配置是必须的 ----------------

# 切记保密你的SECRET_KEY
SECRET_KEY = '<随机生成的任意ASCII字符>'

DATABASES['default'] = dict(
    ENGINE='django.db.backends.postgresql',
    NAME='<数据库名称>',
    USER='postgres',
    PASSWORD='<数据库密码>',
    HOST='127.0.0.1',
    PORT='5432',
)
CACHES['default'] = dict(
    BACKEND='django.core.cache.backends.redis.RedisCache',
    LOCATION='redis://127.0.0.1:6379/<序列号码>',
)

# ---------------- 以下配置是可选的 ----------------

DEBUG = True  # 请勿在生产环境中设置为 True

ALLOWED_HOSTS = ['*']  # DEBUG=False 时必须配置为非空列表

LOGS_DIR.mkdir(exist_ok=True)  # 确保日志目录一定存在

# 把 Django 接收到的所有请求打印到控制台中。
LOGGING['loggers']['django.request']['handlers'] = ['Console', 'RequestRecorder']

# 更多对 settings.py 的自定义覆盖……
```

使用以下代码可以快速生成十个随机 `SECRET_KEY` 备选：

```python
from base64 import b85encode
from random import getrandbits

for _ in range(10):
    soup = getrandbits(64 * 8).to_bytes(64, 'big')
    key = b85encode(soup).decode('ASCII')
    print(key)
```

### 创建应用

在 ./apps 内创建一个带有 serializers.py（-s）和 urls.py（-u）的 Django App 。

```shell
python manage.py newapp APPNAME -su
```
