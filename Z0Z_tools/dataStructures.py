"""
Provides utilities for string extraction from nested data structures
and merges multiple dictionaries containing lists into one dictionary.
"""

from collections.abc import Mapping
from numpy import integer
from numpy.typing import NDArray
from typing import Any
import more_itertools
import python_minifier
import re as regex

def autoDecodingRLE(arrayTarget: NDArray[integer[Any]], addSpaces: bool = False, axisOfOperation: int | None = None) -> str:
	"""Not implemented: Special case, range, start=0
	Not tested: axisOfOperation"""
	if axisOfOperation is None:
		axisOfOperation = 0
	def sliceNDArrayToNestedLists(arraySlice: NDArray[integer[Any]], axisOfOperation: int) -> Any:
		if arraySlice.ndim > 1:
			if (axisOfOperation >= arraySlice.ndim):
				axisOfOperation = -1
			elif abs(axisOfOperation) > arraySlice.ndim:
				axisOfOperation = 0
			return [sliceNDArrayToNestedLists(arraySlice[index], axisOfOperation) for index in range(arraySlice.shape[axisOfOperation])]
		elif arraySlice.ndim == 1:
			arraySliceAsList: list[int | range] = []
			for seriesGrouped in more_itertools.consecutive_groups(arraySlice.tolist()):
				ImaSerious = list(seriesGrouped)
				ImaRange = [range(ImaSerious[0], ImaSerious[-1] + 1)]
				lengthAsList = addSpaces*(len(ImaSerious)-1) + len(python_minifier.minify(str(ImaSerious))) # brackets are proxies for commas
				lengthAsRange = addSpaces*1 + len('*') + len(python_minifier.minify(str(ImaRange)))
				if lengthAsRange < lengthAsList:
					arraySliceAsList += ImaRange
				else:
					arraySliceAsList += ImaSerious

			listRangeAndTuple: list[int | range | tuple[int | range, int]] = []
			for malkovichGrouped in more_itertools.run_length.encode(arraySliceAsList):
				lengthMalkovich = malkovichGrouped[-1]
				malkovichAsList = list(more_itertools.run_length.decode([malkovichGrouped]))
				lengthAsList = addSpaces*(len(malkovichAsList)-1) + len(python_minifier.minify(str(malkovichAsList))) # brackets are proxies for commas
				malkovichMalkovich = f"[{malkovichGrouped[0]}]*{lengthMalkovich}"
				lengthAsMalkovich = len(python_minifier.minify(malkovichMalkovich))
				if lengthAsMalkovich < lengthAsList:
					listRangeAndTuple.append(malkovichGrouped)
				else:
					listRangeAndTuple += malkovichAsList
			return listRangeAndTuple
		return arraySlice

	arrayAsNestedLists = sliceNDArrayToNestedLists(arrayTarget, axisOfOperation)

	arrayAsStr = python_minifier.minify(str(arrayAsNestedLists))

	for _insanity in range(2):
		joinAheadComma = regex.compile("(?<!rang)(?P<joinAhead>,)\\((?P<malkovich>\\d+),(?P<multiple>\\d+)\\)(?P<joinBehind>])")
		joinAheadCommaReplace = "]+[\\g<malkovich>]*\\g<multiple>"
		arrayAsStr = joinAheadComma.sub(joinAheadCommaReplace, arrayAsStr)

		joinBehindComma = regex.compile("(?<!rang)(?P<joinAhead>\\[|^.)\\((?P<malkovich>\\d+),(?P<multiple>\\d+)\\)(?P<joinBehind>,)")
		joinBehindCommaReplace = "[\\g<malkovich>]*\\g<multiple>+["
		arrayAsStr = joinBehindComma.sub(joinBehindCommaReplace, arrayAsStr)

		joinAheadBracket = regex.compile("(?<!rang)(?P<joinAhead>\\[)\\((?P<malkovich>\\d+),(?P<multiple>\\d+)\\)(?P<joinBehind>])")
		joinAheadBracketReplace = "[\\g<malkovich>]*\\g<multiple>"
		arrayAsStr = joinAheadBracket.sub(joinAheadBracketReplace, arrayAsStr)

		joinBothCommas = regex.compile("(?<!rang)(?P<joinAhead>,)\\((?P<malkovich>\\d+),(?P<multiple>\\d+)\\)(?P<joinBehind>,)")
		joinBothCommasReplace = "]+[\\g<malkovich>]*\\g<multiple>+["
		arrayAsStr = joinBothCommas.sub(joinBothCommasReplace, arrayAsStr)

	arrayAsStr = arrayAsStr.replace('range', '*range')

	return arrayAsStr

def stringItUp(*scrapPile: Any) -> list[str]:
	"""
	Convert, if possible, every element in the input data structure to a string. Order is not preserved or readily predictable.

	Parameters:
		*scrapPile: One or more data structures to unpack and convert to strings.
	Returns:
		listStrungUp: A list of string versions of all convertible elements.
	"""
	scrap = None
	listStrungUp: list[str] = []

	def drill(KitKat: Any) -> None:
		if isinstance(KitKat, str):
			listStrungUp.append(KitKat)
		elif isinstance(KitKat, (bool, bytearray, bytes, complex, float, int, memoryview, type(None))):
			listStrungUp.append(str(KitKat))
		elif isinstance(KitKat, dict):
			for broken, piece in KitKat.items():
				drill(broken)
				drill(piece)
		elif isinstance(KitKat, (frozenset, list, range, set, tuple)):
			for kit in KitKat:
				drill(kit)
		elif hasattr(KitKat, '__iter__'): # Unpack other iterables
			for kat in KitKat:
				drill(kat)
		else:
			try:
				sharingIsCaring = KitKat.__str__()
				listStrungUp.append(sharingIsCaring)
			except AttributeError:
				pass
			except TypeError: # "The error traceback provided indicates that there is an issue when calling the __str__ method on an object that does not have this method properly defined, leading to a TypeError."
				pass
			except:
				print(f"\nWoah! I received '{repr(KitKat)}'.\nTheir report card says, 'Plays well with others: Needs improvement.'\n")
				raise
	try:
		for scrap in scrapPile:
			drill(scrap)
	except RecursionError:
		listStrungUp.append(repr(scrap))
	return listStrungUp

def updateExtendPolishDictionaryLists(*dictionaryLists: Mapping[str, list[Any] | set[Any] | tuple[Any, ...]], destroyDuplicates: bool = False, reorderLists: bool = False, killErroneousDataTypes: bool = False) -> dict[str, list[Any]]:
	"""
	Merges multiple dictionaries containing lists into a single dictionary, with options to handle duplicates,
	list ordering, and erroneous data types.

	Parameters:
		*dictionaryLists: Variable number of dictionaries to be merged. If only one dictionary is passed, it will be processed based on the provided options.
		destroyDuplicates (False): If True, removes duplicate elements from the lists. Defaults to False.
		reorderLists (False): If True, sorts the lists. Defaults to False.
		killErroneousDataTypes (False): If True, skips dictionary keys or dictionary values that cause a TypeError during merging. Defaults to False.
	Returns:
		ePluribusUnum: A single dictionary with merged lists based on the provided options. If only one dictionary is passed,
		it will be cleaned up based on the options.
	Note:
		The returned value, `ePluribusUnum`, is a so-called primitive dictionary (`typing.Dict`). Furthermore, every dictionary key is a so-called primitive string (cf. `str()`) and every dictionary value is a so-called primitive list (`typing.List`). If `dictionaryLists` has other data types, the data types will not be preserved. That could have unexpected consequences. Conversion from the original data type to a `typing.List`, for example, may not preserve the order even if you want the order to be preserved.
	"""

	ePluribusUnum: dict[str, list[Any]] = {}

	for dictionaryListTarget in dictionaryLists:
		for keyName, keyValue in dictionaryListTarget.items():
			try:
				ImaStr = str(keyName)
				ImaList = list(keyValue)
				ePluribusUnum.setdefault(ImaStr, []).extend(ImaList)
			except TypeError:
				if killErroneousDataTypes:
					continue
				else:
					raise

	if destroyDuplicates:
		for ImaStr, ImaList in ePluribusUnum.items():
			ePluribusUnum[ImaStr] = list(dict.fromkeys(ImaList))
	if reorderLists:
		for ImaStr, ImaList in ePluribusUnum.items():
			ePluribusUnum[ImaStr] = sorted(ImaList)

	return ePluribusUnum
