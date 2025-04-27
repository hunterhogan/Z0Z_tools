from pathlib import Path
from typing import Any
from tests.conftest import standardizedEqualTo, uniformTestFailureMessage
from Z0Z_tools import dataTabularTOpathFilenameDelimited, findRelativePath, makeDirsSafely, writeStringToHere
import pandas
import pathlib
import pytest
import io

def testDataTabularTOpathFilenameDelimitedBasic(dataframeSample: pandas.DataFrame, pathTmpTesting: pathlib.Path) -> None:
	"""Test basic functionality with DataFrame data."""
	pathOutput = pathTmpTesting / "output.csv"

	# Convert DataFrame to rows and columns
	tableRows: list[list[Any]] = dataframeSample.values.tolist()
	tableColumns: list[str] = dataframeSample.columns.tolist()

	dataTabularTOpathFilenameDelimited(
		pathFilename=pathOutput,
		tableRows=tableRows,
		tableColumns=tableColumns,
		delimiterOutput=','
	)

	assert pathOutput.exists(), uniformTestFailureMessage(True, pathOutput.exists(), "dataTabularTOpathFilenameDelimited", dataframeSample, pathOutput)
	dfRead: pandas.DataFrame = pandas.read_csv(pathOutput)
	pandas.testing.assert_frame_equal(dataframeSample, dfRead)

@pytest.mark.parametrize("delimiterOutput,filenameInfix", [
	(',', 'comma'),
	('\t', 'tab'),
	('|', 'pipe')
])
def testDataTabularTOpathFilenameDelimitedDelimiters(dataframeSample: pandas.DataFrame, pathTmpTesting: pathlib.Path, delimiterOutput: str, filenameInfix: str) -> None:
	"""Test with different delimiters."""
	pathOutput: Path = pathTmpTesting / f"output_{filenameInfix}.txt"

	dataTabularTOpathFilenameDelimited(
		pathFilename=pathOutput,
		tableRows=dataframeSample.values.tolist(),
		tableColumns=dataframeSample.columns.tolist(),
		delimiterOutput=delimiterOutput
	)

	assert pathOutput.exists(), uniformTestFailureMessage(True, pathOutput.exists(), "dataTabularTOpathFilenameDelimited", dataframeSample, pathOutput)
	dfRead: pandas.DataFrame = pandas.read_csv(pathOutput, sep=delimiterOutput)
	pandas.testing.assert_frame_equal(dataframeSample, dfRead)

def testDataTabularTOpathFilenameDelimitedNoHeaders(dataframeSample: pandas.DataFrame, pathTmpTesting: pathlib.Path) -> None:
	"""Test writing data without column headers."""
	pathOutput = pathTmpTesting / "no_headers.csv"

	dataTabularTOpathFilenameDelimited(
		pathFilename=pathOutput,
		tableRows=dataframeSample.values.tolist(),
		tableColumns=[],
		delimiterOutput=','
	)

	assert pathOutput.exists(), uniformTestFailureMessage(True, pathOutput.exists(), "dataTabularTOpathFilenameDelimited", dataframeSample, pathOutput)
	with open(pathOutput) as readStream:
		lines: list[str] = readStream.readlines()
		assert len(dataframeSample) == len(lines), uniformTestFailureMessage(len(dataframeSample), len(lines), "dataTabularTOpathFilenameDelimitedNoHeaders", dataframeSample, pathOutput)

def testDataTabularTOpathFilenameDelimitedEmptyData(pathTmpTesting: pathlib.Path) -> None:
	"""Test writing empty data."""
	pathOutput: Path = pathTmpTesting / "empty.csv"

	dataTabularTOpathFilenameDelimited(
		pathFilename=pathOutput,
		tableRows=[],
		tableColumns=['col1', 'col2'],
		delimiterOutput=','
	)

	assert pathOutput.exists(), uniformTestFailureMessage(True, pathOutput.exists(), "dataTabularTOpathFilenameDelimited", [], pathOutput)
	with open(pathOutput) as readStream:
		lines: list[str] = readStream.readlines()
		assert len(lines) == 1, uniformTestFailureMessage(1, len(lines), "dataTabularTOpathFilenameDelimitedEmptyData", pathOutput)
		assert lines[0].strip() == 'col1,col2', uniformTestFailureMessage('col1,col2', lines[0].strip(), "dataTabularTOpathFilenameDelimitedEmptyData", pathOutput)

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

def testMakeDirsSafelyCreatesParentDirectories(pathTmpTesting: pathlib.Path) -> None:
    nestedDirectory = pathTmpTesting / "sub1" / "sub2"
    filePath = nestedDirectory / "dummy.txt"
    makeDirsSafely(filePath)
    assert nestedDirectory.exists() and nestedDirectory.is_dir(), uniformTestFailureMessage(True, nestedDirectory.exists() and nestedDirectory.is_dir(), "testMakeDirsSafelyCreatesParentDirectories", filePath)

def testMakeDirsSafelyWithIOBaseDoesNotRaise() -> None:
    memoryStream = io.StringIO()
    makeDirsSafely(memoryStream)

def testWriteStringToHereCreatesFileAndWritesContent(pathTmpTesting: pathlib.Path) -> None:
    nestedDirectory = pathTmpTesting / "a" / "b"
    filePath = nestedDirectory / "test.txt"
    writeStringToHere("hello world", filePath)
    assert filePath.exists(), uniformTestFailureMessage(True, filePath.exists(), "testWriteStringToHereCreatesFileAndWritesContent", filePath)
    assert filePath.read_text() == "hello world", uniformTestFailureMessage("hello world", filePath.read_text(), "testWriteStringToHereCreatesFileAndWritesContent", filePath)
