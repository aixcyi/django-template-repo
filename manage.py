#!/usr/bin/env python
"""Django 用于管理任务的命令行实用程序。"""
import os
import sys


def main():
    """Run administrative tasks."""

    # TODO: 根据实际导入的 settings 修改参数二。
    # 例如使用 ./django_template_repo/settings_dev.py 时修改为 'django_template_repo.settings_dev'
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_template_repo.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
