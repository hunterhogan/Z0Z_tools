from numpy.typing import NDArray
from typing import Callable, ParamSpec, TypeVar

callableTargetParameters = ParamSpec('callableTargetParameters')
callableReturnsNDArray = TypeVar('callableReturnsNDArray', bound=Callable[..., NDArray])

def def_asTensor(callableTarget: Callable[callableTargetParameters, NDArray]) -> Callable[callableTargetParameters, NDArray]:
    """
    No-op decorator when torch is not installed.
    Simply returns the original function unchanged.
    """
    return callableTarget
