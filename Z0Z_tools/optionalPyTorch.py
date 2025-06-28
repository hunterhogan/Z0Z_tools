"""Create PyTorch tensor windowing functions."""
from collections.abc import Callable
from torch.types import Device
from typing import Any, TypeVar
from Z0Z_tools import cosineWings, equalPower, halfsine, tukey, WindowingFunction
import torch

callableReturnsNDArray = TypeVar('callableReturnsNDArray', bound=Callable[..., WindowingFunction])

def _convertToTensor(*arguments: Any, callableTarget: callableReturnsNDArray, device: Device, **keywordArguments: Any) -> torch.Tensor:
    arrayTarget = callableTarget(*arguments, **keywordArguments)
    return torch.tensor(data=arrayTarget, dtype=torch.float32, device=device)

def cosineWingsTensor(lengthWindow: int, ratioTaper: float | None=None, device: Device | None=None) -> torch.Tensor:
    """Generate a cosine-tapered windowing function with flat center and tapered ends.

    Parameters
    ----------
    lengthWindow : int
        Total length of the windowing function.
    ratioTaper : float | None = None
        Ratio of taper length to windowing-function length; must be between 0 and 1 inclusive.
    device : Device = torch.device(device='cpu')
        PyTorch device for tensor allocation.

    Returns
    -------
    windowingFunction : WindowingFunction
        Array of windowing coefficients with cosine tapers.

    """
    device = device or torch.device(device='cpu')
    return _convertToTensor(lengthWindow, ratioTaper, callableTarget=cosineWings, device=device)

def equalPowerTensor(lengthWindow: int, ratioTaper: float | None=None, device: Device | None=None) -> torch.Tensor:
    """Generate a windowing function used for an equal power crossfade.

    Parameters
    ----------
    lengthWindow : int
        Total length of the windowing function.
    ratioTaper : float | None = None
        Ratio of taper length to windowing-function length; must be between 0 and 1 inclusive.
    device : Device = torch.device(device='cpu')
        PyTorch device for tensor allocation.

    Returns
    -------
    windowingFunction : WindowingFunction
        Array of windowing coefficients with tapers.

    """
    device = device or torch.device(device='cpu')
    return _convertToTensor(lengthWindow, ratioTaper, callableTarget=equalPower, device=device)

def halfsineTensor(lengthWindow: int, device: Device | None=None) -> torch.Tensor:
    """Generate a half-sine windowing function.

    Parameters
    ----------
    lengthWindow : int
        Total length of the windowing function.
    device : Device = torch.device(device='cpu')
        PyTorch device for tensor allocation.

    Returns
    -------
    windowingFunction : WindowingFunction
        Array of windowing coefficients following half-sine shape.

    """
    device = device or torch.device(device='cpu')
    return _convertToTensor(lengthWindow, callableTarget=halfsine, device=device)

def tukeyTensor(lengthWindow: int, ratioTaper: float | None=None, device: Device | None=None, **keywordArguments: float) -> torch.Tensor:
    """Create a Tukey windowing-function.

    Parameters
    ----------
    lengthWindow : int
        Total length of the windowing function.
    ratioTaper : float | None = None
        Ratio of taper length to windowing-function length; must be between 0 and 1 inclusive.
    **keywordArguments : float
        Additional keyword arguments. `alpha: float | None = None` to be nice and for the Tevye cases: "Tradition!"
    device : Device = torch.device(device='cpu')
        PyTorch device for tensor allocation.

    Returns
    -------
    windowingFunction : WindowingFunction
        Array of Tukey windowing function coefficients.

    """
    device = device or torch.device(device='cpu')
    return _convertToTensor(lengthWindow, ratioTaper, callableTarget=tukey, device=device, **keywordArguments)
