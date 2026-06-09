# Django 存储配置

## SQLite 3

### settings.py

```python
DATABASES = {
    'default': dict(
        BACKEND='storages.backends.s3.S3Storage',
        OPTIONS={
            'access_key': '公钥',
            'secret_key': '私钥',
            'bucket_name': '桶名称',
            'endpoint_url': 'http://127.0.0.1:9000',
            'querystring_auth': False,
            'use_ssl': False,
        },
    ),
}
```
