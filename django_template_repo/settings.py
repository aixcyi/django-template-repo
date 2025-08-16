"""
django_template_repo 的项目设置。

通过 `Django Template Repo <https://github.com/aixcyi/django-template-repo>`_
模板创建；模板本身使用 Django 4.2.5 通过 'django-admin startproject' 命令生成。

- `settings.py 快速配置 <https://docs.djangoproject.com/zh-hans/5.2/topics/settings/>`_
- `settings.py 完整配置列表 <https://docs.djangoproject.com/zh-hans/5.2/ref/settings/>`_
"""

from pathlib import Path

from utils.converters import dict_

BASE_DIR = Path(__file__).resolve().parent.parent
LOGS_DIR = BASE_DIR / 'logs'
APPS_DIR = BASE_DIR / 'apps'

# -------------------------------- 核心 --------------------------------

INSTALLED_APPS = [
    # 内置 app
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # 三方 app
    'rest_framework',

    # 项目 app
    'apps.core.configs.CoreConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

WSGI_APPLICATION = 'django_template_repo.wsgi.application'
ASGI_APPLICATION = 'django_template_repo.asgi.application'

# -------------------------------- 安全 --------------------------------

# https://docs.djangoproject.com/zh-hans/5.2/ref/settings/#secret-key
# TODO: 首次运行前务必将值改为一个随机字符串。可使用 README 给出的方法生成随机密钥，随心挑选一个。
SECRET_KEY = None

DEBUG = False

ALLOWED_HOSTS = [  # DEBUG=False 时必须配置为非空列表
    '.localhost',
    '127.0.0.1',
    '[::1]',
]

# 密码验证
# https://docs.djangoproject.com/zh-hans/5.2/ref/settings/#auth-password-validators
AUTH_PASSWORD_VALIDATORS = [
    dict(
        NAME='django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    ),
    dict(
        NAME='django.contrib.auth.password_validation.MinimumLengthValidator',
        OPTIONS=dict(
            min_length=8,
        ),
    ),
    dict(
        NAME='django.contrib.auth.password_validation.CommonPasswordValidator',
    ),
    dict(
        NAME='django.contrib.auth.password_validation.NumericPasswordValidator',
    ),
]

# -------------------------------- 存储 --------------------------------

# 用户模型
# TODO: 更改用户模型（仅在创建数据库前定义，后续无法更改）。
AUTH_USER_MODEL = 'core.User'

# 数据库
# https://docs.djangoproject.com/zh-hans/5.2/ref/settings/#databases
# https://docs.djangoproject.com/zh-hans/5.2/ref/databases/
DATABASES = {
    'default': dict(
        ENGINE='django.db.backends.sqlite3',
        NAME=':memory:',
    ),
}

# 缓存
# https://docs.djangoproject.com/zh-hans/5.2/ref/settings/#caches
# https://docs.djangoproject.com/zh-hans/5.2/topics/cache/
CACHES = {
    'default': dict(
        BACKEND='django.core.cache.backends.locmem.LocMemCache',
    ),
}

# 静态文件（应配置为对外公开的文件路径）
# https://docs.djangoproject.com/zh-hans/5.2/howto/static-files/
STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'static'

# 用户上传内容
# https://docs.djangoproject.com/zh-hans/5.2/topics/security/#user-uploaded-content-security
MEDIA_URL = 'uploads/'
MEDIA_ROOT = BASE_DIR / 'uploads'

# -------------------------------- 路由 --------------------------------

ROOT_URLCONF = 'django_template_repo.urls'

APPEND_SLASH = False

# -------------------------------- 模板 --------------------------------

TEMPLATES = [
    dict(
        BACKEND='django.template.backends.django.DjangoTemplates',
        DIRS=[
            BASE_DIR / 'templates',
        ],
        APP_DIRS=True,
        OPTIONS={
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    ),
]

# -------------------------------- 日志 --------------------------------

# 日志模块的配置：https://docs.djangoproject.com/zh-hans/5.2/topics/logging/#configuring-logging
# 配置字典架构：https://docs.python.org/zh-cn/3/library/logging.config.html#logging-config-dictschema
LOGGING = dict(
    version=1,
    disable_existing_loggers=False,
    formatters={
        # 格式化器默认配置：https://docs.python.org/zh-cn/3/library/logging.html#logging.Formatter
        'verbose': dict(
            format=(
                '[%(asctime)s] '
                '[%(name)s/%(levelname)s] '
                '[%(process)d,%(processName)s] '
                '[%(thread)d,%(threadName)s] '
                '[%(module)s.%(funcName)s:%(lineno)d]: '
                '%(message)s'
            ),
        ),
        'standard': dict(
            format=(
                '[%(asctime)s] '
                '[%(name)s/%(levelname)s] '
                '[%(module)s.%(funcName)s:%(lineno)d]: '
                '%(message)s'
            ),
        ),
        # 自定义格式化器：https://docs.python.org/zh-cn/3/library/logging.config.html#user-defined-objects
        'printing': {
            '()': 'logging.Formatter',
            'fmt': (
                '[%(asctime)s] '
                '[%(levelname)s] '  # 控制台里没必要打印日志的记录器
                '[%(module)s.%(funcName)s:%(lineno)d]: '
                '%(message)s'
            ),
            '.': {
                'default_time_format': '%H:%M:%S',  # 控制台只打印时间就够了，日期部分没必要打印
            },
        }
    },
    filters={
        # 过滤器：https://docs.python.org/zh-cn/3/library/logging.html#logging.Filter
        'require_debugging': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    # TODO: 模板给出的架构较为简单，请根据项目架构、软硬件配置、业务增量、分析需求等考虑日志架构。
    handlers={
        'monitor': dict_(
            class_='logging.StreamHandler',
            level='INFO',
            filters=[],
            formatter='standard',
        ),
        'console': dict_(
            class_='logging.StreamHandler',
            level='DEBUG',
            filters=['require_debugging'],  # 仅在调试模式下往控制台打印日志
            formatter='printing',
        ),
        # TODO: Windows 下 TimedRotatingFileHandler 可能无法正常轮换日志文件。
        'recorder': dict_(
            class_='logging.handlers.TimedRotatingFileHandler',
            level='INFO',
            formatter='standard',
            filename=LOGS_DIR / 'records.log',
            encoding='UTF-8',
            backupCount=365,
            when='d',
        ),
        'alarmer': dict_(
            class_='logging.handlers.TimedRotatingFileHandler',
            level='WARNING',
            formatter='verbose',
            filename=LOGS_DIR / 'alarms.log',
            encoding='UTF-8',
            backupCount=365,
            when='d',
        ),
    },
    loggers={
        'django': dict(
            level='INFO',
            filters=[],
            handlers=['console'],
        ),
        'django.server': dict(
            level='INFO',
            filters=[],
            handlers=['monitor'],
            propagate=False,
        ),
        'django.request': dict(
            level='INFO',
            filters=[],
            handlers=['console', 'recorder', 'alarmer'],
            propagate=False,
        ),
        'project': dict(
            level='DEBUG',
            filters=[],
            handlers=['console', 'recorder', 'alarmer'],
        ),
    },
)

# -------------------------------- 国际化 --------------------------------
# Internationalization
# https://docs.djangoproject.com/zh-hans/5.2/topics/i18n/

LANGUAGE_CODE = 'zh-hans'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_TZ = True

DATE_FORMAT = 'Y-m-d'
TIME_FORMAT = 'H:i:s'
DATETIME_FORMAT = f'{DATE_FORMAT} {TIME_FORMAT}'

# -------------------------------- 生态框架 --------------------------------

# https://www.django-rest-framework.org/api-guide/settings/
REST_FRAMEWORK = dict(
    DATE_FORMAT='%Y-%m-%d',
    TIME_FORMAT='%H:%M:%S',
    DATETIME_FORMAT='%Y-%m-%d %H:%M:%S',
)

# -------------------------------- 自定义配置 --------------------------------

# ...
