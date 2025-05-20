from typing import TypeVar

TypeSansNone = TypeVar('TypeSansNone')

def raiseIfNone(returnTarget: TypeSansNone | None) -> TypeSansNone:
    if returnTarget is None:
        raise ValueError('Return is None.')
    return returnTarget
"""
Thanks to https://github.com/sobolevn.
https://github.com/python/typing/discussions/1997#discussioncomment-13108399
"""
