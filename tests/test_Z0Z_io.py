import pandas as pd
import pytest
from pathlib import Path
from Z0Z_tools.Z0Z_io import dataTabularTOpathFilenameDelimited, findRelativePath

@pytest.fixture
def dataframeSample():
    return pd.DataFrame({
        'columnA': [1, 2, 3],
        'columnB': ['a', 'b', 'c']
    })

@pytest.fixture
def pathWorkingDirectory(tmp_path):
    """Create a temporary working directory."""
    return tmp_path

def testDataTabularTOpathFilenameDelimitedBasic(dataframeSample, pathWorkingDirectory):
    """Test basic functionality with DataFrame data."""
    pathOutput = pathWorkingDirectory / "output.csv"
    
    # Convert DataFrame to rows and columns
    tableRows = dataframeSample.values.tolist()
    tableColumns = dataframeSample.columns.tolist()
    
    dataTabularTOpathFilenameDelimited(
        pathFilename=pathOutput,
        tableRows=tableRows,
        tableColumns=tableColumns,
        delimiterOutput=','
    )
    
    assert pathOutput.exists()
    dfRead = pd.read_csv(pathOutput)
    pd.testing.assert_frame_equal(dataframeSample, dfRead)

@pytest.mark.parametrize("delimiterOutput,filenameInfix", [
    (',', 'comma'),
    ('\t', 'tab'),
    ('|', 'pipe')
])
def testDataTabularTOpathFilenameDelimitedDelimiters(dataframeSample, pathWorkingDirectory, delimiterOutput, filenameInfix):
    """Test with different delimiters."""
    pathOutput = pathWorkingDirectory / f"output_{filenameInfix}.txt"
    
    dataTabularTOpathFilenameDelimited(
        pathFilename=pathOutput,
        tableRows=dataframeSample.values.tolist(),
        tableColumns=dataframeSample.columns.tolist(),
        delimiterOutput=delimiterOutput
    )
    
    assert pathOutput.exists()
    dfRead = pd.read_csv(pathOutput, sep=delimiterOutput)
    pd.testing.assert_frame_equal(dataframeSample, dfRead)

def testDataTabularTOpathFilenameDelimitedNoHeaders(dataframeSample, pathWorkingDirectory):
    """Test writing data without column headers."""
    pathOutput = pathWorkingDirectory / "no_headers.csv"
    
    dataTabularTOpathFilenameDelimited(
        pathFilename=pathOutput,
        tableRows=dataframeSample.values.tolist(),
        tableColumns=[],
        delimiterOutput=','
    )
    
    assert pathOutput.exists()
    with open(pathOutput, 'r') as readStream:
        lines = readStream.readlines()
        assert len(lines) == len(dataframeSample)

def testDataTabularTOpathFilenameDelimitedEmptyData(pathWorkingDirectory):
    """Test writing empty data."""
    pathOutput = pathWorkingDirectory / "empty.csv"
    
    dataTabularTOpathFilenameDelimited(
        pathFilename=pathOutput,
        tableRows=[],
        tableColumns=['col1', 'col2'],
        delimiterOutput=','
    )
    
    assert pathOutput.exists()
    with open(pathOutput, 'r') as readStream:
        lines = readStream.readlines()
        assert len(lines) == 1
        assert lines[0].strip() == 'col1,col2'

@pytest.fixture
def setupDirectoryStructure(tmp_path):
    """Create a complex directory structure for testing findRelativePath."""
    baseDirectory = tmp_path / "base"
    baseDirectory.mkdir()
    
    # Create nested directories
    for subdir in ["dir1/subdir1", "dir2/subdir2", "dir3/subdir3"]:
        (baseDirectory / subdir).mkdir(parents=True)
    
    # Create some files
    (baseDirectory / "dir1/file1.txt").touch()
    (baseDirectory / "dir2/file2.txt").touch()
    
    return baseDirectory

@pytest.mark.parametrize("pathStart,pathTarget,expectedResult", [
    ("dir1", "dir2", "../dir2"),
    ("dir1/subdir1", "dir2/subdir2", "../../dir2/subdir2"),
    ("dir1", "dir1/subdir1", "subdir1"),
    ("dir3/subdir3", "dir1/file1.txt", "../../dir1/file1.txt"),
])
def testFindRelativePath(setupDirectoryStructure, pathStart, pathTarget, expectedResult):
    """Test findRelativePath with various path combinations."""
    pathStartFull = setupDirectoryStructure / pathStart
    pathTargetFull = setupDirectoryStructure / pathTarget
    
    resultPath = findRelativePath(pathStartFull, pathTargetFull)
    assert resultPath == expectedResult

def testFindRelativePathWithNonexistentPaths(tmp_path):
    """Test findRelativePath with paths that don't exist."""
    pathStart = tmp_path / "nonexistent1"
    pathTarget = tmp_path / "nonexistent2"
    
    resultPath = findRelativePath(pathStart, pathTarget)
    assert resultPath == "../nonexistent2"

def testFindRelativePathWithSamePath(tmp_path):
    """Test findRelativePath when start and target are the same."""
    pathTest = tmp_path / "testdir"
    pathTest.mkdir()
    
    resultPath = findRelativePath(pathTest, pathTest)
    assert resultPath == "."

# @pytest.mark.parametrize("pathStartStr,pathTargetStr", [
#     ("../outside", "dir1"),
#     ("dir1", "../outside"),
# ])
# def testFindRelativePathOutsideBase(setupDirectoryStructure, pathStartStr, pathTargetStr):
#     """Test findRelativePath with paths outside the base directory."""
#     pathStart = setupDirectoryStructure / pathStartStr
#     pathTarget = setupDirectoryStructure / pathTargetStr
    
#     with pytest.raises(ValueError):
#         findRelativePath(pathStart, pathTarget)