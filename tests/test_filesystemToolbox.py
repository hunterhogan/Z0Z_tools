from pathlib import Path
from tests.conftest import uniformTestFailureMessage
from Z0Z_tools import dataTabularTOpathFilenameDelimited, findRelativePath
import pathlib
import pytest

def testDataTabularTOpathFilenameDelimitedBasic(tableSample: tuple[list[list[int | str]], list[str]], pathTmpTesting: pathlib.Path) -> None:
	"""Test basic functionality with table data."""
	tableRows, tableColumns = tableSample
	pathOutput = pathTmpTesting / "output.csv"

	dataTabularTOpathFilenameDelimited(
		pathFilename=pathOutput,
		tableRows=tableRows,
		tableColumns=tableColumns,
		delimiterOutput=','
	)

	assert pathOutput.exists(), uniformTestFailureMessage(True, pathOutput.exists(), "dataTabularTOpathFilenameDelimited", tableRows, pathOutput)
	with open(pathOutput, encoding="utf-8") as readStream:  # noqa: PTH123
		lines = [line.rstrip('\n') for line in readStream]
	assert lines[0] == ','.join(tableColumns), uniformTestFailureMessage(','.join(tableColumns), lines[0], "dataTabularTOpathFilenameDelimited", tableRows, pathOutput)
	for index, row in enumerate(tableRows):
		expectedRow = ','.join(str(value) for value in row)
		assert lines[index + 1] == expectedRow, uniformTestFailureMessage(expectedRow, lines[index + 1], "dataTabularTOpathFilenameDelimited", tableRows, pathOutput)

@pytest.mark.parametrize("delimiterOutput,filenameInfix", [
	(',', 'comma'),
	('\t', 'tab'),
	('|', 'pipe')
])
def testDataTabularTOpathFilenameDelimitedDelimiters(tableSample: tuple[list[list[int | str]], list[str]], pathTmpTesting: pathlib.Path, delimiterOutput: str, filenameInfix: str) -> None:
	"""Test with different delimiters."""
	tableRows, tableColumns = tableSample
	pathOutput: Path = pathTmpTesting / f"output_{filenameInfix}.txt"

	dataTabularTOpathFilenameDelimited(
		pathFilename=pathOutput,
		tableRows=tableRows,
		tableColumns=tableColumns,
		delimiterOutput=delimiterOutput
	)

	assert pathOutput.exists(), uniformTestFailureMessage(True, pathOutput.exists(), "dataTabularTOpathFilenameDelimited", tableRows, pathOutput)
	with open(pathOutput, encoding="utf-8") as readStream:  # noqa: PTH123
		lines = [line.rstrip('\n') for line in readStream]
	assert lines[0] == delimiterOutput.join(tableColumns), uniformTestFailureMessage(delimiterOutput.join(tableColumns), lines[0], "dataTabularTOpathFilenameDelimited", tableRows, pathOutput)
	for index, row in enumerate(tableRows):
		expectedRow = delimiterOutput.join(str(value) for value in row)
		assert lines[index + 1] == expectedRow, uniformTestFailureMessage(expectedRow, lines[index + 1], "dataTabularTOpathFilenameDelimited", tableRows, pathOutput)

def testDataTabularTOpathFilenameDelimitedNoHeaders(tableSample: tuple[list[list[int | str]], list[str]], pathTmpTesting: pathlib.Path) -> None:
	"""Test writing data without column headers."""
	tableRows, _ = tableSample
	pathOutput = pathTmpTesting / "no_headers.csv"

	dataTabularTOpathFilenameDelimited(
		pathFilename=pathOutput,
		tableRows=tableRows,
		tableColumns=[],
		delimiterOutput=','
	)

	assert pathOutput.exists(), uniformTestFailureMessage(True, pathOutput.exists(), "dataTabularTOpathFilenameDelimited", tableRows, pathOutput)
	with open(pathOutput, encoding="utf-8") as readStream:  # noqa: PTH123
		lines: list[str] = [line.rstrip('\n') for line in readStream]
	assert len(tableRows) == len(lines), uniformTestFailureMessage(len(tableRows), len(lines), "dataTabularTOpathFilenameDelimitedNoHeaders", tableRows, pathOutput)

def testDataTabularTOpathFilenameDelimitedEmptyData(pathTmpTesting: pathlib.Path) -> None:
	"""Test writing empty data."""
	pathOutput: Path = pathTmpTesting / "empty.csv"
	tableColumns = ['col1', 'col2']

	dataTabularTOpathFilenameDelimited(
		pathFilename=pathOutput,
		tableRows=[],
		tableColumns=tableColumns,
		delimiterOutput=','
	)

	assert pathOutput.exists(), uniformTestFailureMessage(True, pathOutput.exists(), "dataTabularTOpathFilenameDelimited", [], pathOutput)
	with open(pathOutput, encoding="utf-8") as readStream:  # noqa: PTH123
		lines: list[str] = [line.rstrip('\n') for line in readStream]
	assert len(lines) == 1, uniformTestFailureMessage(1, len(lines), "dataTabularTOpathFilenameDelimitedEmptyData", pathOutput)
	assert lines[0] == ','.join(tableColumns), uniformTestFailureMessage(','.join(tableColumns), lines[0], "dataTabularTOpathFilenameDelimitedEmptyData", pathOutput)

@pytest.mark.parametrize("pathStart,pathTarget,expectedResult", [
	("dir1", "dir2", "../dir2"),
	("dir1/subdir1", "dir2/subdir2", "../../dir2/subdir2"),
	("dir1", "dir1/subdir1", "subdir1"),
	("dir3/subdir3", "dir1/file1.txt", "../../dir1/file1.txt"),
])
def testFindRelativePath(setupDirectoryStructure: pathlib.Path, pathStart: str, pathTarget: str, expectedResult: str) -> None:
	"""Test findRelativePath with various path combinations."""
	pathStartFull: Path = setupDirectoryStructure / pathStart
	pathTargetFull: Path = setupDirectoryStructure / pathTarget

	resultPath: str = findRelativePath(pathStartFull, pathTargetFull)
	assert resultPath == expectedResult, uniformTestFailureMessage(expectedResult, resultPath, "findRelativePath", pathStartFull, pathTargetFull)

def testFindRelativePathWithNonexistentPaths(pathTmpTesting: pathlib.Path) -> None:
	"""Test findRelativePath with paths that don't exist."""
	pathStart: Path = pathTmpTesting / "nonexistent1"
	pathTarget: Path = pathTmpTesting / "nonexistent2"

	resultPath: str = findRelativePath(pathStart, pathTarget)
	assert resultPath == "../nonexistent2", uniformTestFailureMessage("../nonexistent2", resultPath, "findRelativePath", pathStart, pathTarget)

def testFindRelativePathWithSamePath(pathTmpTesting: pathlib.Path) -> None:
	"""Test findRelativePath when start and target are the same."""
	pathTest: Path = pathTmpTesting / "testdir"
	pathTest.mkdir()

	resultPath: str = findRelativePath(pathTest, pathTest)
	assert resultPath == ".", uniformTestFailureMessage(".", resultPath, "findRelativePath", pathTest, pathTest)
