# django template repo

Django 项目模板仓库。

## 特性

- 可以隔离不同环境的配置。
- 更加易读的 `settings.py` 。
- 生成更易读的表名，比如 `order.models.GoodsSKUInfo` 会默认创建 `order_goods_sku_info` 表，而不是 `order_goodsskuinfo` 。
- 预设 `alarms.log` 和 `records.log` 两个日志文件，控制台仅在调试模式才会打印。
- 将 Django App 集中存放在 ./apps 目录下。
- 预设继承 `AbstractUser` 来自定义用户的 `User` 模型（放在 `core` 这个app里）。
- 通过 `__all__` 约束包公开的符号。

## 兼容性

以 Django 4.2 为基准创建，目前兼容 Django 3.x｜4.x｜5.x，兼容 Python 3.6 - 3.13。

> [!IMPORTANT]
> 如果您使用 Python 3.11 以前（不含）的版本，需要修改
> `commons.views.MeowModelViewSet` 内的处理逻辑。

## 结构

### 目录结构（按依赖先后排序）

- `./apps` 存放项目内的所有 Django App。
- `./commons` 存放对于框架的定制，或仅适用于单个项目的工具。
- `./django_template_repo` 存放 Django Settings、总路由等配置。
- `./utils` 存放（可以跨项目的）通用工具。

### 日志记录器

- `""` 根记录器。
  - `project` 项目内的根记录器。
  - `django` 框架使用的根记录器，由框架自带。
    - `django.server` 服务器部分的日志。不向上传递。
    - `django.request` 请求部分的日志。不向上传递。
    - 更多内置的记录器见[默认的日志定义](https://docs.djangoproject.com/zh-hans/5.2/ref/logging/#default-logging-definition)。

### 日志处理器

| 名称         | 目标                   | 级别        | 格式 | 用途                     |
|------------|----------------------|-----------|----|------------------------|
| `monitor`  | 控制台                  | `INFO`    | 标准 | 专供 `django.server` 使用。 |
| `console`  | 控制台                  | `DEBUG`   | 标准 | 处理所有控制台打印。             |
| `recorder` | `./logs/records.log` | `INFO`    | 标准 | 处理所有非调试日志。             |
| `alarmer`  | `./logs/alarms.log`  | `WARNING` | 详细 | 处理所有警告和异常。             |

- 日志处理器默认无条件触发。`console` 仅在 `DEBUG = True` 时触发。
- `console` 的打印格式基于标准格式，但去除了时刻中的日期部分。

## 用法

> [!TIP]
> [我应该使用哪个版本的 Python 来配合 Django？](https://docs.djangoproject.com/zh-hans/5.2/faq/install/#what-python-version-can-i-use-with-django)

1. [从模板创建仓库（GitHub）](https://docs.github.com/zh/repositories/creating-and-managing-repositories/creating-a-repository-from-a-template)；
2. 克隆刚刚创建的仓库；
3. 重命名文件夹 ./django_template_repo 及所有引用和字符串为你的 **项目名**；
4. 根据需要创建并切换虚拟环境；
5. `pip install -r requirements.txt` 安装依赖；
6. 在 ./django_template_repo 中创建自定义配置文件 settings_dev.py；
7. 查找所有以 `TODO` 开头的注释，并按照提示进行修改；
8. `python manage.py runserver` 运行项目。

### 配置设置

> - [Django Settings 快速配置](https://docs.djangoproject.com/zh-hans/5.2/topics/settings/)
> - [Django Settings 完整配置列表](https://docs.djangoproject.com/zh-hans/5.2/ref/settings/)
> - [Django REST Framework Settings](https://www.django-rest-framework.org/api-guide/settings/)

./django_template_repo/settings_*.py 不会被纳入版本管理，
你可以通过创建不同命名的配置来实现生产环境和开发环境的隔离，
比如用 `settings_dev.py` 配置开发环境，用 `settings_prod.py` 来配置生产环境。

仅 `SECRET_KEY` 是必须进行配置的。
使用以下代码可以快速生成随机 `SECRET_KEY` 以备选择：

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
[`startapp`](https://docs.djangoproject.com/zh-hans/5.2/ref/django-admin/#startapp)
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

[注意事项](https://docs.djangoproject.com/zh-hans/5.2/ref/databases/#postgresql-notes)

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

[注意事项](https://docs.djangoproject.com/zh-hans/5.2/ref/databases/#mysql-notes)

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

[注意事项](https://docs.djangoproject.com/zh-hans/5.2/ref/databases/#oracle-notes)

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

[注意事项](https://docs.djangoproject.com/zh-hans/5.2/ref/databases/#sqlite-notes)

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

[设置缓存](https://docs.djangoproject.com/zh-hans/5.2/topics/cache/#redis)

```python
CACHES = {
    'default': dict(
        BACKEND='django.core.cache.backends.redis.RedisCache',
        LOCATION='redis://127.0.0.1:6379/0',
    ),
}
```

### 调试环境配置快速参考

```python
from django_template_repo.settings import *

DEBUG = True
SECRET_KEY = '<Z~Bhb@?39U0EcX31IKEQ^93GlQt-o-x8QXH#sE7=Ci?gJ4J49nOKir?WMR3`EhyjOt%uivqAZ!Ka;uL'
ALLOWED_HOSTS = [
    '*',
]
DATABASES['default'] = dict(
    ENGINE='django.db.backends.postgresql',
    NAME='django_template_repo',
    USER='postgres',
    PASSWORD='postgres',
    HOST='127.0.0.1',
    PORT='5432',
)
CACHES['default'] = dict(
    BACKEND='django.core.cache.backends.redis.RedisCache',
    LOCATION='redis://127.0.0.1:6379/11',
)
LOGS_DIR.mkdir(exist_ok=True)
MEDIA_ROOT.mkdir(exist_ok=True)
STATIC_ROOT.mkdir(exist_ok=True)
```
