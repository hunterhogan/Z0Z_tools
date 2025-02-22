"""If `torch` is installed, this module creates tensor versions of the windowing functions."""
from collections.abc import Callable
from numpy import ndarray, dtype, float64
from torch.types import Device
from typing import Any, ParamSpec, Protocol, TypeVar, cast
import sys
import torch

callableTargetParameters = ParamSpec('callableTargetParameters')
callableReturnsNDArray = TypeVar('callableReturnsNDArray', bound=Callable[..., ndarray[tuple[int], dtype[float64]]])

class callableAsTensor(Protocol[callableTargetParameters]):
	__name__: str
	__doc__: str | None
	__module__: str
	def __call__(self, device: Device = ..., *args: callableTargetParameters.args, **kwargs: callableTargetParameters.kwargs) -> torch.Tensor: ...

# GitHub #2
def def_asTensor(callableTarget: Callable[callableTargetParameters, ndarray[tuple[int], dtype[float64]]]) -> Callable[callableTargetParameters, ndarray[tuple[int], dtype[float64]]]:
	"""
	Decorator that creates a tensor version of a numpy array-returning function.
	The tensor version will be available with a 'Tensor' suffix.

	Example:
		@def_asTensor
		def window(n: int) -> ndarray[Tuple[int], dtype[float64]]: ...

		This creates:
		- window(n: int) -> ndarray[Tuple[int], dtype[float64]]
		- windowTensor(n: int, device: torch.device = torch.device('cpu')) -> torch.Tensor
	"""
	def convertToTensor(*args: Any, device: Device = torch.device(device='cpu'), **kwargs: Any) -> torch.Tensor:
		arrayTarget = callableTarget(*args, **kwargs)
		return torch.tensor(data=arrayTarget, dtype=torch.float32, device=device)

	# Get the module where the decorated function is defined
	moduleTarget = sys.modules[callableTarget.__module__]

	# Cast and set the convertToTensor function with proper name
	callableAsTensorTarget = cast(callableAsTensor[callableTargetParameters], convertToTensor)
	callableAsTensorTarget.__name__ = callableTarget.__name__ + "Tensor"
	callableAsTensorTarget.__doc__ = f"""
	Tensor version of {callableTarget.__name__}.
	Same parameters as the original function, plus an optional device parameter.

	Additional Parameters:
		device: torch.device = torch.device('cpu')
			The device to place the tensor on.

	Returns:
		torch.Tensor: The result as a PyTorch tensor.
	"""
	callableAsTensorTarget.__module__ = callableTarget.__module__

	# Add to the module's __all__ if it exists
	if hasattr(moduleTarget, '__all__'):
		moduleTarget.__all__.append(callableAsTensorTarget.__name__)

	# Set in both globals and module dict
	setattr(moduleTarget, callableAsTensorTarget.__name__, callableAsTensorTarget)

	return callableTarget
