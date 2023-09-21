# django template repo

Django 4.2 项目的模板仓库。

## 优点

- 通过 settings_*.py 隔离不同环境的配置。
- 很容易看出来 settings 里大部分配置字典的哪些 key 是固定的。
- 生成更易读的表名，比如 `order.models.GoodsSKUInfo` 会创建 `order_goods_sku_info` 表。
- 自带 alarms.log、records.log、requests.log 三个日志配置。
- 自定义 `User` 模型（放在自带的 `core` app里）。
- 将 Django App 集中存放在 ./apps 目录下。

## 用法

> [我应该使用哪个版本的 Python 来配合 Django？](https://docs.djangoproject.com/zh-hans/4.2/faq/install/#what-python-version-can-i-use-with-django)

1. [从模板创建仓库 - GitHub](https://docs.github.com/zh/repositories/creating-and-managing-repositories/creating-a-repository-from-a-template) ；
2. 使用 `git clone my_project git@github.com:YOURNAME/PROJECT.git` 克隆刚刚创建的仓库；
3. 根据需要创建虚拟环境，并切换到虚拟环境中；
4. 在项目配置目录（也就是 settings.py 所在的文件夹）中创建自己的配置文件 settings_dev.py ；
5. 将根目录下的 manage.py 里的环境变量 `DJANGO_SETTINGS_MODULE` 修改为 `配置目录.settings_dev` ；
6. 使用 `python manage.py runserver 127.0.0.1:8080` 运行项目。

## 配置模板

settings_*.py 模板如下：

```python
# 导入自己项目下的 settings
from django_template_repo.settings import *

# ---------------- 以下配置是必须的 ----------------

# 不可公开的密钥，Django 用来计算各种带盐的哈希。
SECRET_KEY = '<随机生成的任意ASCII字符>'

# 模板没有 default 项，而 Django 默认只使用 default 项，所以必须配置。
DATABASES['default'] = dict(
    ENGINE='django.db.backends.postgresql',
    NAME='<数据库名称>',
    USER='postgres',
    PASSWORD='<数据库密码>',
    HOST='127.0.0.1',
    PORT='5432',
)

# 模板没有 default 项，而 Django 默认只使用 default 项，所以必须配置。
CACHES['default'] = dict(
    BACKEND='django.core.cache.backends.redis.RedisCache',
    LOCATION='redis://127.0.0.1:6379/<序列号码>',
)

# ---------------- 以下配置是可选的 ----------------

# 开启调试模式。
DEBUG = True  # 生产环境中墙裂不推荐开启！！！

# 空列表只接收本地IP的请求。在本地环境中，如果请求要回调到本地，则需要允许特定IP的请求。
# 以下配置表示允许来自任意IP的请求，生产环境中不推荐这么做！
ALLOWED_HOSTS = ['*']

# 确保日志目录一定存在
LOGS_DIR.mkdir(exist_ok=True)

# 这个配置用于把 Django 接收到的所有请求打印到控制台中。
LOGGING['loggers']['django.request']['handlers'] = ['Console', 'RequestRecorder']

# 更多对 settings.py 的自定义覆盖……
```
