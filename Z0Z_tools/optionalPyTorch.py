from collections.abc import Callable
from torch.types import Device
from typing import Any, TypeVar
from Z0Z_tools import cosineWings, equalPower, halfsine, tukey, WindowingFunction
import torch

callableReturnsNDArray = TypeVar('callableReturnsNDArray', bound=Callable[..., WindowingFunction])

def _convertToTensor(*arguments: Any, callableTarget: callableReturnsNDArray, device: Device, **keywordArguments: Any) -> torch.Tensor:
    arrayTarget = callableTarget(*arguments, **keywordArguments)
    return torch.tensor(data=arrayTarget, dtype=torch.float32, device=device)

def cosineWingsTensor(lengthWindow: int, ratioTaper: float | None=None, device: Device=torch.device(device='cpu')) -> torch.Tensor:
    return _convertToTensor(lengthWindow, ratioTaper, callableTarget=cosineWings, device=device)

def equalPowerTensor(lengthWindow: int, ratioTaper: float | None=None, device: Device=torch.device(device='cpu')) -> torch.Tensor:
    return _convertToTensor(lengthWindow, ratioTaper, callableTarget=equalPower, device=device)

def halfsineTensor(lengthWindow: int, device: Device=torch.device(device='cpu')) -> torch.Tensor:
    return _convertToTensor(lengthWindow, callableTarget=halfsine, device=device)

def tukeyTensor(lengthWindow: int, ratioTaper: float | None=None, device: Device=torch.device(device='cpu'), **keywordArguments: float) -> torch.Tensor:
    return _convertToTensor(lengthWindow, ratioTaper, callableTarget=tukey, device=device, **keywordArguments)