from pathlib import Path

from django.conf import settings
from django.core.management.templates import TemplateCommand

TMP_URLS = '''
from django.urls import path

urlpatterns = [
    # Set your urls here.
]
'''[1:]

TMP_SERIALIZERS = '''
from rest_framework import serializers

# Create your serializers here.
'''[1:]


class Command(TemplateCommand):
    help = (
        "Creates a Django app directory structure for the given app name in "
        "the current directory or optionally in the given directory."
    )
    missing_args_message = "You must provide an application name."

    def add_arguments(self, parser):
        super().add_arguments(parser)
        parser.add_argument(
            "--with-serializers",
            "-s",
            dest="with_serializers",
            action="store_true",
            help="一并创建一个 serializers.py 文件。",
        )
        parser.add_argument(
            "--with-urls",
            "-u",
            dest="with_urls",
            action="store_true",
            help="一并创建一个 urls.py 文件。",
        )

    def handle(self, **options):
        with_serializers = options.pop("with_serializers")
        with_urls = options.pop("with_urls")
        app_name = options.pop("name")
        target = Path(options.pop("directory") or (settings.APPS_DIR / app_name)).absolute()
        target.mkdir(exist_ok=True)
        super().handle("app", app_name, target, **options)

        app_conf = target / "apps.py"
        if app_conf.exists():
            app_conf.rename(target / "configs.py")

        self.handle_with_template(target, with_urls, "urls.py", TMP_URLS)
        self.handle_with_template(target, with_serializers, "serializers.py", TMP_SERIALIZERS)

    def handle_with_template(self, app_dir: Path, with_template: bool, filename, content):
        if not with_template:
            return
        fp = app_dir / filename
        fp.touch(exist_ok=True)
        fp.write_text(content, encoding='UTF-8')
