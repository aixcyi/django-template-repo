__all__ = [
    'Cacher',
    'cacher',
]

from typing import Any

from django.core.cache import caches


class Cacher:
    def __init__(self, name='default'):
        self.target = caches[name]

    def __contains__(self, key: str) -> bool:
        return self.target.has_key(key)

    def __getitem__(self, key: str) -> Any:
        return self.target.get(key)

    def __setitem__(self, key: tuple[str, slice | int], value) -> None:
        name, timeout = key
        match timeout:
            case int():
                self.target.set(name, value, timeout=timeout)
            case slice():
                self.target.set(name, value, timeout=timeout.start * 3600 + timeout.stop * 60 + timeout.step)
            case _:
                raise TypeError(f'Cacher 不接受 {type(timeout).__name__} 类型的 timeout。')

    def __delitem__(self, key: str) -> None:
        self.target.delete(key)


cacher = Cacher()
