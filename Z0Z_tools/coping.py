from typing import TypeVar

TypeSansNone = TypeVar('TypeSansNone')

def raiseIfNone(returnTarget: TypeSansNone | None) -> TypeSansNone:
    if returnTarget is None:
        raise ValueError('Return is None.')
    return returnTarget
