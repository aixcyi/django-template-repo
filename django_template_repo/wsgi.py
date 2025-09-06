"""
django_template_repo 项目的 WSGI 配置。

这里通过一个模块级别的变量 ``application`` 对外公开了 WSGI 的构造方法。
更多信息参见话题 `如何使用 WSGI 进行部署 <https://docs.djangoproject.com/zh-hans/5.2/howto/deployment/wsgi/>`_
"""

import os

from django.core.wsgi import get_wsgi_application

# TODO: 根据实际导入的 settings 修改参数二。
# 例如使用 ./django_template_repo/settings_dev.py 时修改为 'django_template_repo.settings_dev'
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_template_repo.settings')

application = get_wsgi_application()
