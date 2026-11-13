"""Functions that exist to carry one signature each, named by their parameters; every body returns `None`."""
from __future__ import annotations

def signatureEmpty() -> None:
	return None

def signatureX(x: object) -> None:
	return None

def signatureXDefault1(x: object = 1) -> None:
	return None

def signatureArgs(*args: object) -> None:
	return None

def signatureKwargs(**kwargs: object) -> None:
	return None

def signatureXArgs(x: object, *args: object) -> None:
	return None

def signatureXYDefault1Kwargs(x: object, y: object = 1, **kwargs: object) -> None:
	return None

def signatureABDefaultsCD(a: object, b: object, c: object = 3, d: object = 4) -> None:
	return None

def signatureXYArgsKwargs(x: object, y: object, *args: object, **kwargs: object) -> None:
	return None

def signatureFuncDefaultNone(func: object = None) -> None:
	return None

def signatureXPositionalOnly(x: object, /) -> None:
	return None

def signatureXKeywordOnly(*, x: object) -> None:
	return None

def signatureLikePartial(func: object, /, *args: object, **keywords: object) -> None:
	return None
