import torch
from collections.abc import Callable
from numpy import dtype, float64, ndarray
from torch.types import Device as Device
from typing import ParamSpec, Protocol, TypeVar

callableTargetParameters = ParamSpec('callableTargetParameters')
callableReturnsNDArray = TypeVar('callableReturnsNDArray', bound=Callable[..., ndarray[tuple[int], dtype[float64]]])

class callableAsTensor(Protocol[callableTargetParameters]):
    __doc__: str | None
    __module__: str
    def __call__(self, device: Device = ..., *args: callableTargetParameters.args, **kwargs: callableTargetParameters.kwargs) -> torch.Tensor: ...

def def_asTensor(callableTarget: Callable[callableTargetParameters, ndarray[tuple[int], dtype[float64]]]) -> Callable[callableTargetParameters, ndarray[tuple[int], dtype[float64]]]: ...
