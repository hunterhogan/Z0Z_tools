"""If `torch` is not installed, this module prevents errors."""
from collections.abc import Callable
from numpy import ndarray, dtype, float64
from typing import ParamSpec, TypeVar

callableTargetParameters = ParamSpec('callableTargetParameters')
callableReturnsNDArray = TypeVar('callableReturnsNDArray', bound=Callable[..., ndarray[tuple[int], dtype[float64]]])

def def_asTensor(callableTarget: Callable[callableTargetParameters, ndarray[tuple[int], dtype[float64]]]) -> Callable[callableTargetParameters, ndarray[tuple[int], dtype[float64]]]:
	return callableTarget
