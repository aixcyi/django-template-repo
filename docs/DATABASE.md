# Django 数据库配置

## SQLite 3

- [配置注意事项](https://docs.djangoproject.com/zh-hans/5.2/ref/databases/#sqlite-notes)

### settings.py

使用内存数据库：

```python
DATABASES = {
    'default': dict(
        ENGINE='django.db.backends.sqlite3',
        NAME=':memory:',
    ),
}
```

使用文件数据库：

```python
from django_template_repo.settings import PROJECT_DIR

DATABASES = {
    'default': dict(
        ENGINE='django.db.backends.sqlite3',
        NAME=PROJECT_DIR / 'db.sqlite3',
    ),
}
```

## PostgreSQL

- [配置注意事项](https://docs.djangoproject.com/zh-hans/5.2/ref/databases/#postgresql-notes)

### settings.py

```python
DATABASES = {
    'default': dict(
        ENGINE='django.db.backends.postgresql',
        NAME='数据库名称',
        USER='postgres',
        PASSWORD='账号密码',
        HOST='127.0.0.1',
        PORT='5432',
    ),
}
```

## MySQL

- [配置注意事项](https://docs.djangoproject.com/zh-hans/5.2/ref/databases/#mysql-notes)

### settings.py

```python
DATABASES = {
    'default': dict(
        ENGINE='django.db.backends.mysql',
        NAME='数据库名称',
        USER='root',
        PASSWORD='账号密码',
        HOST='127.0.0.1',
        PORT='3306',
    ),
}
```

## Oracle

- [配置注意事项](https://docs.djangoproject.com/zh-hans/5.2/ref/databases/#oracle-notes)

### settings.py

```python
DATABASES = {
    'default': dict(
        ENGINE='django.db.backends.oracle',
        NAME='数据库名称',
        USER='system',
        PASSWORD='账号密码',
        HOST='127.0.0.1',
        PORT='1521',
    ),
}
```
