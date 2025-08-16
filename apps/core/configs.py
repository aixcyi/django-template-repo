from django.apps import AppConfig


class CoreConfig(AppConfig):
    name = 'apps.core'
    label = 'core'
    verbose_name = 'Project Core'
    # TODO: 创建新的 Django App 前请平衡数据库行宽与数据增量，选择 AutoField 或 BigAutoField。
    default_auto_field = 'django.db.models.AutoField'
