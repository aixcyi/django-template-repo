# Django 缓存配置

## Redis

从 Django 4.0 开始可以使用自带的 [`RedisCache`](https://docs.djangoproject.com/zh-hans/5.2/topics/cache/#redis)
作为缓存后端来使用 Redis：

```python
CACHES = {
    'default': dict(
        BACKEND='django.core.cache.backends.redis.RedisCache',
        LOCATION='redis://127.0.0.1:6379/0',
    ),
}
```

Django 4.0 以前，或者需要直接访问 Redis 的连接对象来使用更多[命令](https://redis.io/docs/latest/commands/)，可以安装
[`django-redis`](https://pypi.org/project/django-redis/)：

```python
CACHES = {
    'default': dict(
        BACKEND='django_redis.cache.RedisCache',
        LOCATION='redis://127.0.0.1:6379/0',
        OPTIONS=dict(
            CLIENT_CLASS='django_redis.client.DefaultClient',
        )
    )
}
```

如果需要更高的性能，可以与 [`hiredis`](https://pypi.org/project/hiredis/) 搭配使用：

```python
CACHES = {
    'default': dict(
        BACKEND='django_redis.cache.RedisCache',
        LOCATION='redis://127.0.0.1:6379/0',
        OPTIONS=dict(
            CLIENT_CLASS='django_redis.client.DefaultClient',
            PARSER_CLASS='redis.connection.HiredisParser',
        )
    )
}
```

但注意，如果使用 `hiredis` 5.0 及以上的版本，需要这样：

```python
CACHES = {
    'default': dict(
        BACKEND='django_redis.cache.RedisCache',
        LOCATION='redis://127.0.0.1:6379/0',
        OPTIONS=dict(
            CLIENT_CLASS='django_redis.client.DefaultClient',
            PARSER_CLASS='redis.connection._HiredisParser',
        )
    )
}
```
