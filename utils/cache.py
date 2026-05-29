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

    def __getitem__(self, item: str | tuple[str, Any]) -> Any:
        match item:
            case str(key):
                return self.target.get(key)
            case [str(key), default]:
                return self.target.get(key, default=default)
            case _:
                raise TypeError('无法解析 Cacher.__getitem__() 的参数。')

    def __setitem__(self, item: tuple[str, slice | int], value) -> None:
        match item:
            case [str(key), int(timeout)]:
                self.target.set(key, value, timeout=timeout)
            case [str(key), slice() as t]:
                self.target.set(key, value, timeout=(t.start or 0) * 3600 + (t.stop or 0) * 60 + (t.step or 0))
            case [str(), t]:
                raise TypeError(f'Cacher.__setitem__() 不接受 {type(t).__name__} 类型的 timeout 值。')
            case [key, _]:
                raise TypeError(f'Cacher.__setitem__() 不接受 {type(key).__name__} 类型的 key 值。')
            case _:
                raise TypeError('无法解析 Cacher.__setitem__() 的参数。')

    def __delitem__(self, key: str) -> None:
        self.target.delete(key)


cacher = Cacher()
