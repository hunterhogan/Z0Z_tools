"""If `torch` is not installed, this module prevents errors."""
from numpy.typing import NDArray
from typing import Callable, ParamSpec, TypeVar
callableTargetParameters = ParamSpec('callableTargetParameters')
callableReturnsNDArray = TypeVar('callableReturnsNDArray', bound=Callable[..., NDArray])

def def_asTensor(callableTarget: Callable[callableTargetParameters, NDArray]) -> Callable[callableTargetParameters, NDArray]:
	return callableTarget
