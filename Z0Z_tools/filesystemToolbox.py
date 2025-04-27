"""
Provides basic file I/O utilities such as writing tabular data to a file
and computing a canonical relative path from one location to another.
"""

from collections.abc import Iterable
from os import PathLike
from typing import Any
import io
import pathlib

def dataTabularTOpathFilenameDelimited(pathFilename: str | PathLike[Any], tableRows: Iterable[Iterable[Any]], tableColumns: Iterable[Any], delimiterOutput: str = '\t') -> None:
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

def findRelativePath(pathSource: str | PathLike[Any], pathDestination: str | PathLike[Any]) -> str:
	"""
	Find a relative path from source to destination, even if they're on different branches.

	Parameters:
		pathSource: The starting path
		pathDestination: The target path

	Returns:
		stringRelativePath: A string representation of the relative path from source to destination
	"""
	pathSource = pathlib.Path(pathSource).resolve()
	pathDestination = pathlib.Path(pathDestination).resolve()

	if pathSource.is_file() or not pathSource.suffix == '':
		pathSource = pathSource.parent

	# Split destination into parent path and filename if it's a file
	pathDestinationParent: pathlib.Path = pathDestination.parent if pathDestination.is_file() or not pathDestination.suffix == '' else pathDestination
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
			pathlib.Path(pathFilename).parent.mkdir(parents=True, exist_ok=True)
		except OSError:
			pass
