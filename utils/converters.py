__all__ = [
    'dict_',
]


def dict_(**kwargs) -> dict:
    """
    去除键名尾缀的 ``_`` 符号，用于键名为 Python 关键字时不能用 ``dict()`` 定义键值对的问题。
    """
    return {
        (k[:-1] if k.endswith('_') else k): v
        for k, v in kwargs.items()
    }
