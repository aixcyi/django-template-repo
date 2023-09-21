"""
django_template_repo 的项目设置。

通过 `Django Template Repo <https://github.com/aixcyi/django-template-repo>`_
模板创建；模板本身使用 Django 4.2.5 通过 'django-admin startproject' 命令生成。

- `settings.py 快速配置 <https://docs.djangoproject.com/zh-hans/4.2/topics/settings/>`_
- `settings.py 完整配置列表 <https://docs.djangoproject.com/zh-hans/4.2/ref/settings/>`_
"""

from pathlib import Path

# 项目根目录
BASE_DIR = Path(__file__).resolve().parent.parent

# -------------------------------- 核心 --------------------------------

# 私有密钥，切勿公开！
SECRET_KEY = ''

# 切勿在生产环境开启调试！
DEBUG = False

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
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

ROOT_URLCONF = 'django_template_repo.urls'

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

WSGI_APPLICATION = 'django_template_repo.wsgi.application'

# -------------------------------- 存储 --------------------------------

# 主键字段的默认类型
# https://docs.djangoproject.com/zh-hans/4.2/ref/settings/#default-auto-field
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# 数据库
# https://docs.djangoproject.com/zh-hans/4.2/ref/settings/#databases
DATABASES = {
    'template_postgresql': dict(
        ENGINE='django.db.backends.postgresql',
        NAME='<数据库名称>',
        USER='postgres',
        PASSWORD='',
        HOST='127.0.0.1',
        PORT='5432',
    ),
    'template_mysql': dict(
        ENGINE='django.db.backends.mysql',
        NAME='<数据库名称>',
        USER='root',
        PASSWORD='',
        HOST='127.0.0.1',
        PORT='3306',
    ),
    'template_oracle': dict(
        ENGINE='django.db.backends.oracle',
        NAME='<数据库名称>',
        USER='system',
        PASSWORD='',
        HOST='127.0.0.1',
        PORT='1521',
    ),
    'template_sqlite3': dict(
        ENGINE='django.db.backends.sqlite3',
        NAME=BASE_DIR / '[数据库名称].sqlite3',
    ),
}

# -------------------------------- 安全 --------------------------------

ALLOWED_HOSTS = []

# 密码验证
# https://docs.djangoproject.com/zh-hans/4.2/ref/settings/#auth-password-validators
AUTH_PASSWORD_VALIDATORS = [
    dict(
        NAME='django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    ),
    dict(
        NAME='django.contrib.auth.password_validation.MinimumLengthValidator',
        OPTIONS={
            "min_length": 8,
        },
    ),
    dict(
        NAME='django.contrib.auth.password_validation.CommonPasswordValidator',
    ),
    dict(
        NAME='django.contrib.auth.password_validation.NumericPasswordValidator',
    ),
]

# --------------------------------

# 静态文件相关配置 (CSS, JavaScript, Images)
# https://docs.djangoproject.com/zh-hans/4.2/howto/static-files/

STATIC_URL = 'static/'

# -------------------------------- 国际化 --------------------------------
# Internationalization
# https://docs.djangoproject.com/zh-hans/4.2/topics/i18n/

LANGUAGE_CODE = 'zh-hans'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True
