from base64 import b85encode
from random import getrandbits

from django.core.management import BaseCommand


class Command(BaseCommand):
    help = (
        "生成一定数量的、符合 settings.SECRET_KEY 要求的随机字符串以供挑选。"
    )

    def add_arguments(self, parser):
        super().add_arguments(parser)
        parser.add_argument(
            "--quantity",
            "-n",
            dest="quantity",
            type=int,
            default=10,
            help="要生成的字符串个数，每行一个字符串，默认是 10 个。",
        )

    def handle(self, **options):
        quantity = options.pop("quantity")
        tips = f' SECRET_KEY x{quantity} '.center(80, '-')

        print(tips)
        for _ in range(quantity):
            soup = getrandbits(64 * 8).to_bytes(64, 'big')
            key = b85encode(soup).decode('ASCII')
            print(key)
