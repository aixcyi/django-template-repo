import keyword
import os
import sys
from contextlib import suppress
from pathlib import Path

TEMPLATE_NAME = 'django_template_repo'
PROJECT_ROOT = Path(__file__).resolve().parent.parent
PATTERNS = [
    'api/**/*.py',
    'apps/**/*.py',
    'commons/**/*.py',
    f'{TEMPLATE_NAME}/**/*.py',
    'docs/**/*.md',
    'utils/**/*.py',
    '.gitignore',
    'CHANGELOG.md',
    'README.md',
    'manage.py',
]


# noinspection PyPep8Naming
def main():
    _, name, *_ = *sys.argv, None
    directoryName = name or input(f'将配置目录从 "{TEMPLATE_NAME}" 重命名为：')
    if not directoryName.isidentifier() or keyword.iskeyword(directoryName):
        print(f'配置目录 "{directoryName}" 不符合 Python 包命名规则。')
        return

    for pattern in PATTERNS:
        for file in PROJECT_ROOT.glob(pattern):
            content = file.read_text(encoding='utf-8')
            if TEMPLATE_NAME in content:
                file.write_text(content.replace(TEMPLATE_NAME, directoryName), encoding='utf-8')
                print(f'已修改 {file}')

    directoryOld = PROJECT_ROOT / TEMPLATE_NAME
    directoryNew = PROJECT_ROOT / directoryName
    if directoryOld.is_dir():
        if directoryOld.exists():
            directoryOld.rename(directoryNew)
            print(f'重命名 {directoryOld}{os.sep}')
            print(f'为目录 {directoryNew}{os.sep}')
        else:
            print(f'已存在同名目录 {directoryNew}{os.sep}')
            return

    print('-' * 32)
    print('完毕。')


if __name__ == '__main__':
    with suppress(KeyboardInterrupt):
        main()
