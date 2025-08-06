__all__ = [
    'case_camel_to_snake',
]

import re


def case_camel_to_snake(name: str) -> str:
    """
    将类似 ``CombineOrderSKUModel`` 大小写形式的字符串
    转换为 ``combine_order_sku_model`` 。
    """
    # "CombineOrderSKUModel"
    # -> "Combine OrderSKU Model"
    # -> "Combine Order SKU Model"
    # -> "combine_order_sku_model"
    mid = re.sub('(.)([A-Z][a-z]+)', r'\1 \2', name)
    words = re.sub('([a-z0-9])([A-Z])', r'\1 \2', mid)
    return '_'.join(word.lower() for word in words.split())
