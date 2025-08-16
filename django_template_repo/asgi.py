"""
ASGI config for django_template_repo project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/zh-hans/5.2/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application

# TODO: 根据实际导入的 settings 修改参数二。
# 例如使用 ./django_template_repo/settings_dev.py 时修改为 'django_template_repo.settings_dev'
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_template_repo.settings')

application = get_asgi_application()
