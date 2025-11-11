from importlib import import_module
from pathlib import Path

from django.conf import settings
from django.core.management import CommandError
from django.core.management.templates import TemplateCommand


class Command(TemplateCommand):
    help = '基于项目定制模板，在 settings 配置的 APP 目录下创建一个指定名称的 Django App。'
    missing_args_message = '请为 App 起一个名字。'

    target: Path

    def add_arguments(self, parser):
        parser.add_argument('name', help='App 名称，必须是一个包名。')

    def handle(self, **options):
        if not hasattr(settings, 'PROJECT_ROOT'):
            raise CommandError('请在 settings 中配置 PROJECT_ROOT 指明当前项目的根目录。')
        if not hasattr(settings, 'APPS_ROOT'):
            raise CommandError('请在 settings 中配置 APPS_ROOT 指明 Django App 的存放目录。')

        template_dir = (settings.APPS_DIR / 'template').absolute()
        self.target = (settings.APPS_DIR / options.pop('name')).absolute()

        try:
            module = self.target.relative_to(settings.PROJECT_DIR)
        except ValueError:
            module = self.target.name

        super().handle(
            # TemplateCommand 必须的参数：
            'app',
            name=self.target.name,
            target=str(self.target),
            template=str(template_dir),
            extensions=['py'],
            files=[],
            # Django Template Repo 定义的参数：
            app_module=str(module).replace('/', '.').replace('\\', '.'),
            **options,
        )

    def validate_name(self, name, name_or_dir='name'):
        if name is None:
            raise CommandError(self.missing_args_message)

        if not name.isidentifier():
            raise CommandError(f"'{name}' 不符合 Python 标识符命名规则。")

        try:
            import_module(name)
        except ImportError:
            pass
        else:
            raise CommandError(f"'{name}' 与一个 Python 模块的名称冲突了，请为 App 另起一个名字吧。")

        # super().handle() 的 target 在不为 None 时必须存在，
        # 而如果提前创建则会被导入，无法通过前面几行逻辑，
        # 但它又不可以不校验可否导入，因此只能放在这里创建。
        self.target.mkdir(exist_ok=True)
