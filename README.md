# Django Template Repo

一个 Django 项目模板。基于 `django-admin` 默认模板定制，倾向于配合 Django REST Framework 进行前后端分离开发。

## 特性

### 架构与布局

- 为隔离不同环境（开发环境、测试环境、生产环境）而设计。
- 预设两个日志文件 `./logs/alarms.log` 和 `./logs/records.log`，控制台仅在调试模式才会打印。
- 生成更易读的表名，比如 `apps.order.models.GoodsSKUInfo` 会默认创建 `order_goods_sku_info` 表，而不是 `order_goodsskuinfo` 。

### 代码与格式

- 拥有更加易查、易读的 `settings.py` 。
- 预设（Django 推荐）继承 `AbstractUser` 来自定义 `apps.core.models.User` 模型。
- 潜在改动位置通过 `TODO` 开头的注释进行提示，且均位于单独一行，方便清理。
- 每个项目都可单独定制 Django App 模板。

### 业务与功能

- 简易第二方 API 请求与响应封装。
- 简易微信 API 封装。
- 默认启用 Django REST Framework 的 Token 认证。

## 结构

### 目录结构（按依赖先后排序）

| 目录                       | 含义   | 描述                                    |
|--------------------------|------|---------------------------------------|
| `./logs`                 | 日志文件 | 存储运行日志。完全按照[用法](#用法)配置后，首次运行时自动生成。    |
| `./static`               | 静态文件 | 存储项目静态文件。完全按照[用法](#用法)配置后，首次运行时自动生成。  |
| `./uploads`              | 上传文件 | 存储用户上传的文件。完全按照[用法](#用法)配置后，首次运行时自动生成。 |
| `./utils`                | 通用工具 | 跨项目的、通用的工具或代码。                        |
| `./scripts`              | 脚本工具 | 提供给模板使用者的脚本工具。                        |
| `./api`                  | 封装接口 | 与第三方和第二方交互的请求接口及响应处理。                 |
| `./commons`              | 定制工具 | 仅适用于当前项目的工具或对框架的定制。                   |
| `./django_template_repo` | 项目配置 | Django Settings、总路由等。                 |
| `./apps`                 | 业务   | 项目内的所有 Django App。                    |
| `./apps/template`        | 模板   | 项目内 Django App 的模板。                   |
| `./apps/core`            | 核心工具 | 被项目内其它所有 Django App 依赖的工具或代码。         |

### 日志记录器

- `""` 根记录器。
  - `project` 项目内的根记录器。
    - `api` 第二第三方 API 相关日志的记录器，专供 `./api/` 下的代码调用。
  - `django` 框架使用的根记录器，由框架自带。
    - `django.server` 服务器部分的日志。不向上传递。
    - `django.request` 请求部分的日志。不向上传递。
    - `django.db.backends` 数据库后端的日志。不向上传递。
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

> [!IMPORTANT]  
> 从 Django Template Repo v5.0 开始，默认采用 [uv](https://docs.astral.sh/uv/) 管理项目、维护依赖、说明用法。

### 第一步：克隆仓库

可以在 GitHub
中[从模板创建仓库](https://docs.github.com/zh/repositories/creating-and-managing-repositories/creating-a-repository-from-a-template)，然后通过以下命令克隆到本地。

```shell
git clone 你的仓库地址 项目新名称
```

如果不希望创建一个新的 GitHub 仓库，或者不使用 GitHub 平台，可以使用以下命令得到只有一条历史记录的本地仓库。

```shell
git clone --depth 1 git@github.com:aixcyi/django-template-repo.git 项目新名称
```

### 第二步：安装依赖

> [!TIP]  
> [我应该使用哪个版本的 Python 来配合 Django？](https://docs.djangoproject.com/zh-hans/5.2/faq/install/#what-python-version-can-i-use-with-django)

模板更推荐使用 [uv](https://docs.astral.sh/uv/) 安装管理 Python 和虚拟环境，执行以下命令

```shell
uv --version
```

之后打印出如下格式的文本即可说明已经成功安装：

```text
uv 0.11.16 (135a36367 2026-05-21 x86_64-pc-windows-msvc)
```

现在以 Python 3.10 为例创建并激活虚拟环境：

```shell
uv venv --python 3.10
```

`pyproject.toml` 中的依赖版本仅仅只是最低要求，你可以根据喜好与实际需求来调整。

```shell
uv sync
```

如果需要更丰富的开发体验，可以选择一并安装可选依赖：

```shell
uv sync --extra dev
```

以上两条命令二选一执行即可。

### 第三步：命名项目

1. 修改 `./pyproject.toml` 下 `[project]` 一节中的 `name` 为你的项目名称、`version` 为你的项目版本号。
2. 模板的 Django Settings 目录位于 `./django_template_repo/`，可以执行以下命令来一键更名（需要符合 Python 包命名规则）。

```shell
uv run scripts/fit.py
```

### 第四步：配置环境

> [!NOTE]  
> Django 文档：[Settings 快速配置](https://docs.djangoproject.com/zh-hans/5.2/topics/settings/)  
> Django 文档：[Settings 完整配置列表](https://docs.djangoproject.com/zh-hans/5.2/ref/settings/)  
> Django REST Framework 文档 [Settings 部分](https://www.django-rest-framework.org/api-guide/settings/)

> 这一步以 PostgreSQL 和 Redis 为例，其它参见[数据库配置](/docs/DATABASE.md)和[缓存配置](/docs/CACHES.md)。

修改 `./django_template_repo/settings.py` 下的 `DATABASES` 和 `CACHES`
并根据需要删去除了 `default` 之外的其它配置（这么做是为了统一开发、测试、生产环境）：

```python
DATABASES = {
    'default': dict(
        ENGINE='django.db.backends.postgresql',
        NAME='django_template_repo',
        USER='postgres',
        PASSWORD='postgres',
        HOST='127.0.0.1',
        PORT='5432',
    ),
}
CACHES = {
    'default': dict(
        BACKEND='django.core.cache.backends.redis.RedisCache',
        LOCATION='redis://127.0.0.1:6379/0',
    ),
}
```

创建 `./django_template_repo/settings_dev.py` 用于配置开发环境：

> 执行 `uv run manage.py genkey -n 20` 可以快速生成 20 个 `SECRET_KEY` 以供挑选。

```python
from django_template_repo.settings import *

DEBUG = True
SECRET_KEY = '<Z~Bhb@?39U0EcX31IKEQ^93GlQt-o-x8QXH#sE7=Ci?gJ4J49nOKir?WMR3`EhyjOt%uivqAZ!Ka;uL'
ALLOWED_HOSTS = ['*']
DATABASES['default']['NAME'] = 'django_template_repo'
DATABASES['default']['USER'] = 'postgres'
DATABASES['default']['PASSWORD'] = 'postgres'
CACHES['default']['LOCATION'] = 'redis://127.0.0.1:6379/0'
LOGS_DIR.mkdir(exist_ok=True)  # 日志目录
MEDIA_ROOT.mkdir(exist_ok=True)  # 用户上传目录
STATIC_ROOT.mkdir(exist_ok=True)  # 静态文件目录
```

创建 `./django_template_repo/settings_prod.py` 用于配置生产环境：

> [!IMPORTANT]  
> 切记，生产环境中的
> [`SECRET_KEY`](https://docs.djangoproject.com/zh-hans/5.2/ref/settings/#std-setting-SECRET_KEY)
> 应当与其它 **所有环境** 都不相同。

```python
from django_template_repo.settings import *

DEBUG = False
SECRET_KEY = 'Yl#}JDJ>>>tWhU{z1#yPmgu_Js^h6*SVqd*DYSE{FpNi8vtY;5W!gJq;?793?5jfF+IdH0z>&WPRG=-?'
DATABASES['default']['NAME'] = 'django_template_repo'
DATABASES['default']['USER'] = 'aliyum'
DATABASES['default']['PASSWORD'] = 'fox-yum-cha'
CACHES['default']['LOCATION'] = 'redis://127.0.0.1:6379/0'
```

### 第五步：定制项目

1. 按照喜好或需要删除或改编这个 README 文件；
2. 查找所有以 `TODO: ` 开头的注释，并按照提示根据实际需要进行修改。

### 第六步：运行项目

执行以下命令运行项目：

```shell
uv run manage.py runserver
```

## 工作流

### 创建 Django App

在 `settings.APPS_ROOT` 指定的目录下按照模板 `./apps/template`
创建一个 Django App（将 `<APPNAME>` 替换为你需要的 App 包名）：

```shell
uv run manage.py addapp <APPNAME>
```

> [!NOTE]  
> `./apps/template` 是独属于 **当前项目** 的 Django App 模板，与
> django-admin 的 `startapp` 所使用的模板互不影响；默认配备了
> Django REST Framework 的 `serializers.py`
> 以及 `urls.py`，可以按照喜好或需求改动，同时为了适配统一存储，将
> `apps.py` 更名为 `configs.py`。

### 生成迁移文件

```shell
uv run manage.py makemigrations
```

### 执行迁移

```shell
uv run manage.py migrate
```

### 运行项目

可以默认在 `127.0.0.1:8000` 下运行：

```shell
uv run manage.py runserver
```

也可以用指定的 IP 和端口运行：

```shell
uv run manage.py runserver 127.0.0.1:22333
```

### 格式化代码

格式化项目内的所有代码：

```shell
ruff format
```

格式化指定文件或文件夹：

```shell
ruff format ./
```

### 检查代码

```shell
ruff check
```

### 添加依赖

以 `pandas` 为例：

```shell
uv pip install pandas
```

记得一并修改 `pyproject.toml` 。

### 同步项目依赖

执行过 `uv pip install` 安装包或 `uv pip uninstall` 卸载包之后，需要手动修改
`pyproject.toml` 的 `project.dependencies`，然后执行：

```shell
uv sync
```

如果还需要安装 `project.optional-dependencies` 下的可选依赖（以 `dev` 组为例），可以改为执行：

```shell
uv sync --extra dev
```

## 兼容性

仅对 Django 最新一个 LTS 的正式发布版本兼容，项目版本号跟随 major 变动，Python 兼容性也跟随变动，详情可见
[Django FAQ](https://docs.djangoproject.com/zh-hans/5.2/faq/install/#what-python-version-can-i-use-with-django)
或
[《Django 兼容性简表》](https://blog.navifox.net/refs/nav/django#compatibility)。
