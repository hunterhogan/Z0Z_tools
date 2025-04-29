"""
Provides basic file I/O utilities such as writing tabular data to a file
and computing a canonical relative path from one location to another.
"""

from collections.abc import Callable, Iterable
from os import PathLike
from pathlib import Path, PurePath
from types import ModuleType
from typing import Any
from Z0Z_tools import str_nameDOTname
import importlib
import importlib.util
import io

def dataTabularTOpathFilenameDelimited(pathFilename: PathLike[Any] | PurePath, tableRows: Iterable[Iterable[Any]], tableColumns: Iterable[Any], delimiterOutput: str = '\t') -> None:
	"""
	Writes tabular data to a delimited file. This is a low-quality function: you'd probably be better off with something else.

	Parameters:
		pathFilename: The path and filename where the data will be written.
		tableRows: The rows of the table, where each row is a list of strings or floats.
		tableColumns: The column headers for the table.
		delimiterOutput (tab): The delimiter to use in the output file. Defaults to *tab*.
	Returns:
		None:

	This function still exists because I have not refactored `analyzeAudio.analyzeAudioListPathFilenames()`. The structure of
	that function's returned data is easily handled by this function. See https://github.com/hunterhogan/analyzeAudio
	"""
	with open(pathFilename, 'w', newline='') as writeStream:
		# Write headers if they exist
		if tableColumns:
			writeStream.write(delimiterOutput.join(map(str, tableColumns)) + '\n')

		# Write rows
		for row in tableRows:
			writeStream.write(delimiterOutput.join(map(str, row)) + '\n')

def findRelativePath(pathSource: PathLike[Any] | PurePath, pathDestination: PathLike[Any] | PurePath) -> str:
	"""
	Find a relative path from source to destination, even if they're on different branches.

	Parameters:
		pathSource: The starting path
		pathDestination: The target path

	Returns:
		stringRelativePath: A string representation of the relative path from source to destination
	"""
	pathSource = Path(pathSource).resolve()
	pathDestination = Path(pathDestination).resolve()

	if pathSource.is_file() or not pathSource.suffix == '':
		pathSource = pathSource.parent

	# Split destination into parent path and filename if it's a file
	pathDestinationParent: Path = pathDestination.parent if pathDestination.is_file() or not pathDestination.suffix == '' else pathDestination
	filenameFinal: str = pathDestination.name if pathDestination.is_file() or not pathDestination.suffix == '' else ''

	# Split both paths into parts
	partsSource: tuple[str, ...] = pathSource.parts
	partsDestination: tuple[str, ...] = pathDestinationParent.parts

	# Find the common prefix
	indexCommon = 0
	for partSource, partDestination in zip(partsSource, partsDestination):
		if partSource != partDestination:
			break
		indexCommon += 1

	# Build the relative path
	partsUp: list[str] = ['..'] * (len(partsSource) - indexCommon)
	partsDown = list(partsDestination[indexCommon:])

	# Add the filename if present
	if filenameFinal:
		partsDown.append(filenameFinal)

	return '/'.join(partsUp + partsDown) if partsUp + partsDown else '.'

def importLogicalPath2Callable(logicalPathModule: str_nameDOTname, identifier: str, packageIdentifierIfRelative: str | None = None) -> Callable[..., Any]:
	"""
	Import a callable object (function or class) from a module based on its logical path.

	This function imports a module using `importlib.import_module()` and then retrieves a specific attribute (function,
	class, or other object) from that module.

	Parameters
	----------
	logicalPathModule
		The logical path to the module, using dot notation (e.g., 'package.subpackage.module').
	identifier
		The name of the callable object to retrieve from the module.
	packageIdentifierIfRelative : None
		The package name to use as the anchor point if `logicalPathModule` is a relative import. If None, absolute
		import is assumed.

	Returns
	-------
	Callable[..., Any]
		The callable object (function, class, etc.) retrieved from the module.
	"""
	# TODO The return type is not accurate.
	moduleImported: ModuleType = importlib.import_module(logicalPathModule, packageIdentifierIfRelative)
	# TODO I want a semantic way, not `getattr`, but there might not be a semantic way.
	return getattr(moduleImported, identifier)

def importPathFilename2Callable(pathFilename: PathLike[Any] | PurePath, identifier: str, moduleIdentifier: str | None = None) -> Callable[..., Any]:
	"""
	Load a callable (function, class, etc.) from a Python file.

	This function imports a specified Python file as a module, extracts a callable object from it by name, and returns
	that callable.

	Parameters
	----------
	pathFilename
		Path to the Python file to import.
	identifier
		Name of the callable to extract from the imported module.
	moduleIdentifier
		Name to use for the imported module. If None, the filename stem is used.

	Returns
	-------
	Callable[..., Any]
		The callable object extracted from the imported module.

	Raises
	------
	ImportError
		If the file cannot be imported or the importlib specification is invalid.
	AttributeError
		If the identifier does not exist in the imported module.
	"""
	# TODO The return type is not accurate.
	pathFilename = Path(pathFilename)

	importlibSpecification = importlib.util.spec_from_file_location(moduleIdentifier or pathFilename.stem, pathFilename)
	if importlibSpecification is None or importlibSpecification.loader is None: raise ImportError(f"I received\n\t`{pathFilename = }`,\n\t`{identifier = }`, and\n\t`{moduleIdentifier = }`.\n\tAfter loading, \n\t`importlibSpecification` {'is `None`' if importlibSpecification is None else 'has a value'} and\n\t`importlibSpecification.loader` is unknown.")

	moduleImported_jk_hahaha: ModuleType = importlib.util.module_from_spec(importlibSpecification)
	importlibSpecification.loader.exec_module(moduleImported_jk_hahaha)
	# TODO I want a semantic way, not `getattr`, but there might not be a semantic way.
	return getattr(moduleImported_jk_hahaha, identifier)

def makeDirsSafely(pathFilename: Any) -> None:
	"""
	Creates parent directories for a given path safely.

	This function attempts to create all necessary parent directories for a given path.
	If the directory already exists or if there's an OSError during creation, it will
	silently continue without raising an exception.

	Parameters:
		pathFilename: A path-like object or file object representing the path
			for which to create parent directories. If it's an IO stream object,
			no directories will be created.

	Returns:
		None:
	"""
	if not isinstance(pathFilename, io.IOBase):
		try:
			Path(pathFilename).parent.mkdir(parents=True, exist_ok=True)
		except OSError:
			pass

def writeStringToHere(this: str, pathFilename: PathLike[Any] | PurePath) -> None:
	pathFilename = Path(pathFilename)
	makeDirsSafely(pathFilename)
	pathFilename.write_text(str(this))
