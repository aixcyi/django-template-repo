# Django Template Repo

Django 项目模板，基于 `django-admin` 默认模板定制，倾向于配合 Django REST Framework 进行前后端分离开发。

## 特性

- 架构上：
  - 为隔离不同环境（开发环境、测试环境、生产环境）的而设计。
  - 预设两个日志文件 `./logs/alarms.log` 和 `./logs/records.log`，控制台仅在调试模式才会打印。
  - 内置的 `utils.models.SnakeModel` 可生成更易读的表名，比如 `apps.order.models.GoodsSKUInfo` 会默认创建 `order_goods_sku_info` 表，而不是 `order_goodsskuinfo` 。
- 代码上：
  - 拥有更加易查、易读的 `settings.py` 。
  - 预设（Django 推荐）继承 `AbstractUser` 来自定义 `apps.core.models.User` 模型。
  - 潜在改动位置通过 `TODO` 开头的注释进行提示，且均位于单独一行，方便清理。
  - 通过 `__all__` 约束包公开的符号。

## 兼容性

以 Django 4.2 为底创建，兼容 Django 5.x｜4.x｜3.x，兼容
Python 3.6 - 3.13，可以参见[《Django 兼容性简表》](https://blog.navifox.net/refs/nav/django#compatibility)。

## 结构

### 目录结构

| 目录（按依赖先后排序）              | 含义   | 描述                            |
|--------------------------|------|-------------------------------|
| `./utils`                | 通用工具 | 跨项目的、通用的工具或代码。                |
| `./commons`              | 定制工具 | 仅适用于当前项目的工具，或对框架的定制。          |
| `./django_template_repo` | 项目配置 | Django Settings、总路由等。         |
| `./apps`                 | 业务   | 项目内的所有 Django App。            |
| `./apps/core`            | 核心工具 | 被项目内其它所有 Django App 依赖的工具或代码。 |
| `./logs`                 | 日志   | 使用[配置模板](#配置模板)可在首次运行时自动生成。   |

### 日志记录器

- `""` 根记录器。
  - `project` 项目内的根记录器。
  - `django` 框架使用的根记录器，由框架自带。
    - `django.server` 服务器部分的日志。不向上传递。
    - `django.request` 请求部分的日志。不向上传递。
    - 更多内置的记录器见 [Django 默认的日志定义](https://docs.djangoproject.com/zh-hans/5.2/ref/logging/#default-logging-definition)。

### 日志处理器

| 名称         | 目标                   | 级别        | 格式 | 用途                     |
|------------|----------------------|-----------|----|------------------------|
| `monitor`  | 控制台                  | `INFO`    | 标准 | 专供 `django.server` 使用。 |
| `console`  | 控制台                  | `DEBUG`   | 标准 | 处理所有控制台打印。             |
| `recorder` | `./logs/records.log` | `INFO`    | 标准 | 处理所有非调试日志。             |
| `alarmer`  | `./logs/alarms.log`  | `WARNING` | 详细 | 处理所有警告和异常。             |

- 日志处理器默认无条件触发。`console` 仅在 `settings.DEBUG = True` 时触发。
- `console` 的打印格式基于标准格式，但去除了时刻中的日期部分。

## 用法

### 1、克隆仓库

可以在 GitHub
中[从模板创建仓库](https://docs.github.com/zh/repositories/creating-and-managing-repositories/creating-a-repository-from-a-template)，然后通过以下命令克隆到本地。

```shell
git clone 你的仓库地址 项目新名称
```

如果不希望创建一个新的 GitHub 仓库，可以使用以下命令得到只有一条历史记录的本地仓库。

```shell
git clone --depth 1 git@github.com:aixcyi/django-template-repo.git 项目新名称
```

### 2、安装依赖

> [!TIP]  
> [我应该使用哪个版本的 Python 来配合 Django？](https://docs.djangoproject.com/zh-hans/5.2/faq/install/#what-python-version-can-i-use-with-django)

1. 根据需要创建并切换到虚拟环境；
2. 根据需要调整 `./requirements.txt` 中的依赖包版本；
3. 执行 `pip install -r ./requirements.txt` 安装依赖。

### 3、定制代码

1. 将 `./django_template_repo` 重命名为你的 **项目名**（需要符合 Python 包命名规则）；
2. 查找所有以 `TODO` 开头的注释，并按照提示根据实际需要进行修改；
3. 根据需要创建自定义配置文件 ./django_template_repo/settings_dev.py（也可以是其它名字，但建议放在同一个文件夹）。

### 4、配置 Settings

可以参见下方的[配置模板](#配置模板)选取代码快速配置。

> [!NOTE]  
> Django 文档：[Settings 快速配置](https://docs.djangoproject.com/zh-hans/5.2/topics/settings/)  
> Django 文档：[Settings 完整配置列表](https://docs.djangoproject.com/zh-hans/5.2/ref/settings/)  
> Django REST Framework 文档 [Settings 部分](https://www.django-rest-framework.org/api-guide/settings/)

./django_template_repo/settings_*.py 不会被纳入版本管理，
你可以通过创建不同命名的配置来实现生产环境和开发环境的隔离，
比如用 `settings_dev.py` 配置开发环境，用 `settings_prod.py` 来配置生产环境。

执行以下命令可以快速生成任意个 `SECRET_KEY` 以供挑选：

```shell
python manage.py genkey -n 20
```

### 5、创建 Django App（可选）

执行以下命令可以创建一个带有 `serializers.py` 和 `urls.py` 的 Django App。

```shell
python manage.py newapp <APPNAME> -su
```

### 6、运行项目

执行以下命令运行项目：

```shell
python manage.py runserver
```

## 配置模板

### 开发环境

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

# 确保目录一定存在
LOGS_DIR.mkdir(exist_ok=True)  # 日志目录
MEDIA_ROOT.mkdir(exist_ok=True)  # 用户上传目录
STATIC_ROOT.mkdir(exist_ok=True)  # 静态文件目录
```

### 生产环境

```python
from django_template_repo.settings import *

DEBUG = False
SECRET_KEY = 'Yl#}JDJ>>>tWhU{z1#yPmgu_Js^h6*SVqd*DYSE{FpNi8vtY;5W!gJq;?793?5jfF+IdH0z>&WPRG=-?'
ALLOWED_HOSTS = [  # DEBUG=False 时必须配置为非空列表
    '.localhost',
    '127.0.0.1',
    '[::1]',
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
