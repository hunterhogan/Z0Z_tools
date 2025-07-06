"""File system and module import utilities.

This module provides basic file I/O utilities such as writing tabular data to files, computing canonical relative paths, importing
callables from modules, and safely creating directories.

"""

from collections.abc import Iterable
from os import PathLike
from pathlib import Path, PurePath
from typing import Any, TypeVar

归个 = TypeVar('归个')

def dataTabularTOpathFilenameDelimited(pathFilename: PathLike[Any] | PurePath, tableRows: Iterable[Iterable[Any]], tableColumns: Iterable[Any], delimiterOutput: str = '\t') -> None:
	r"""Write tabular data to a delimited file.

	This is a low-quality function: you'd probably be better off with something else.

	Parameters
	----------
	pathFilename : PathLike[Any] | PurePath
		The path and filename where the data will be written.
	tableRows : Iterable[Iterable[Any]]
		The rows of the table, where each row is a list of strings or floats.
	tableColumns : Iterable[Any]
		The column headers for the table.
	delimiterOutput : str = '\t'
		The delimiter to use in the output file.

	Notes
	-----
	This function still exists because I have not refactored `analyzeAudio.analyzeAudioListPathFilenames()`. The structure of that
	function's returned data is easily handled by this function. See https://github.com/hunterhogan/analyzeAudio

	"""
	with open(pathFilename, 'w', newline='', encoding='utf-8') as writeStream:  # noqa: PTH123
		# Write headers if they exist
		if tableColumns:
			writeStream.write(delimiterOutput.join(map(str, tableColumns)) + '\n')

		# Write rows
		writeStream.writelines(delimiterOutput.join(map(str, row)) + '\n' for row in tableRows)

def findRelativePath(pathSource: PathLike[Any] | PurePath, pathDestination: PathLike[Any] | PurePath) -> str:
	"""Find a relative path from source to destination, even if they're on different branches.

	Parameters
	----------
	pathSource : PathLike[Any] | PurePath
		The starting path.
	pathDestination : PathLike[Any] | PurePath
		The target path.

	Returns
	-------
	stringRelativePath : str
		A string representation of the relative path from source to destination.

	"""
	pathSource = Path(pathSource).resolve()
	pathDestination = Path(pathDestination).resolve()

	if pathSource.is_file() or pathSource.suffix != '':
		pathSource = pathSource.parent

	# Split destination into parent path and filename if it's a file
	pathDestinationParent: Path = pathDestination.parent if pathDestination.is_file() or pathDestination.suffix != '' else pathDestination
	filenameFinal: str = pathDestination.name if pathDestination.is_file() or pathDestination.suffix != '' else ''

	# Split both paths into parts
	partsSource: tuple[str, ...] = pathSource.parts
	partsDestination: tuple[str, ...] = pathDestinationParent.parts

	# Find the common prefix
	indexCommon = 0
	for partSource, partDestination in zip(partsSource, partsDestination, strict=False):
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
