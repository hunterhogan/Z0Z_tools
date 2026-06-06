from __future__ import annotations

from typing import Any, TYPE_CHECKING
import pathlib
import pytest
import shutil
import uuid

if TYPE_CHECKING:
	from collections.abc import Callable, Generator

pathDataSamples = pathlib.Path("tests/dataSamples")
pathTmpRoot: pathlib.Path = pathDataSamples / "tmp"

registerOfTemporaryFilesystemObjects: set[pathlib.Path] = set()

def registrarRecordsTmpObject(path: pathlib.Path) -> None:
	"""The registrar adds a tmp file to the register."""
	registerOfTemporaryFilesystemObjects.add(path)

def registrarDeletesTmpObjects() -> None:
	"""The registrar cleans up tmp files in the register."""
	for pathTmp in sorted(registerOfTemporaryFilesystemObjects, reverse=True):
		try:
			if pathTmp.is_file():
				pathTmp.unlink(missing_ok=True)
			elif pathTmp.is_dir():
				shutil.rmtree(pathTmp, ignore_errors=True)
		except Exception as ERRORmessage:
			print(f"Warning: Failed to clean up {pathTmp}: {ERRORmessage}")  # noqa: T201
	registerOfTemporaryFilesystemObjects.clear()

@pytest.fixture(scope="session", autouse=True)
def setupTeardownTmpObjects() -> Generator[None]:
	"""Auto-fixture to setup test data directories and cleanup after."""
	pathDataSamples.mkdir(exist_ok=True)
	pathTmpRoot.mkdir(exist_ok=True)
	yield
	registrarDeletesTmpObjects()

@pytest.fixture
def pathTmpTesting(request: pytest.FixtureRequest) -> pathlib.Path:
	pathTmp = pathTmpRoot / str(uuid.uuid4().hex)
	pathTmp.mkdir(parents=True, exist_ok=False)

	registrarRecordsTmpObject(pathTmp)
	return pathTmp

@pytest.fixture
def pathFilenameTmpTesting(request: pytest.FixtureRequest) -> pathlib.Path:
	try:
		extension: str = request.param
	except AttributeError:
		extension = ".txt"

	uuidHex: str = uuid.uuid4().hex
	subpath: str = uuidHex[0:-8]
	filenameStem: str = uuidHex[-8:None]

	pathFilenameTmp = pathlib.Path(pathTmpRoot, subpath, filenameStem + extension)
	pathFilenameTmp.parent.mkdir(parents=True, exist_ok=False)

	registrarRecordsTmpObject(pathFilenameTmp)
	return pathFilenameTmp

@pytest.fixture
def mockTemporaryFiles(monkeypatch: pytest.MonkeyPatch, pathTmpTesting: pathlib.Path) -> None:
	"""Mock all temporary filesystem operations to use pathTmpTesting."""
	monkeypatch.setattr('tempfile.mkdtemp', lambda *a, **k: str(pathTmpTesting))  # pyright: ignore[reportUnknownLambdaType, reportUnknownArgumentType]
	monkeypatch.setattr('tempfile.gettempdir', lambda: str(pathTmpTesting))
	monkeypatch.setattr('tempfile.mkstemp', lambda *a, **k: (0, str(pathTmpTesting)))  # pyright: ignore[reportUnknownLambdaType, reportUnknownArgumentType]

@pytest.fixture
def setupDirectoryStructure(pathTmpTesting: pathlib.Path) -> pathlib.Path:
	"""Create a complex directory structure for testing findRelativePath."""
	baseDirectory = pathTmpTesting / "base"
	baseDirectory.mkdir()

	for subdir in ["dir1/subdir1", "dir2/subdir2", "dir3/subdir3"]:
		(baseDirectory / subdir).mkdir(parents=True)

	(baseDirectory / "dir1/file1.txt").touch()
	(baseDirectory / "dir2/file2.txt").touch()

	return baseDirectory

@pytest.fixture
def tableSample() -> tuple[list[list[int | str]], list[str]]:
	tableColumns: list[str] = ['columnA', 'columnB']
	tableRows: list[list[int | str]] = [
		[5, 'N'],
		[8, 'E'],
		[13, 'S'],
	]
	return tableRows, tableColumns

def uniformTestFailureMessage(expected: Any, actual: Any, functionName: str, *arguments: Any, **keywordArguments: Any) -> str:
	"""Format assertion message for any test comparison."""
	listArgumentComponents: list[str] = [str(parameter) for parameter in arguments]
	listKeywordComponents: list[str] = [f"{key}={value}" for key, value in keywordArguments.items()]
	joinedArguments: str = ', '.join(listArgumentComponents + listKeywordComponents)

	return (f"\nTesting: `{functionName}({joinedArguments})`\n"
			f"Expected: {expected}\n"
			f"Got: {actual}")

def standardizedEqualTo(expected: Any, functionTarget: Callable[..., Any], *arguments: Any, **keywordArguments: Any) -> None:
	"""Template for most tests to compare the actual outcome with the expected outcome."""
	if type(expected) == type[Exception]:  # noqa: E721
		messageExpected: str = expected.__name__
	else:
		messageExpected = expected

	try:
		messageActual = actual = functionTarget(*arguments, **keywordArguments)
	except Exception as actualError:
		messageActual: str = type(actualError).__name__
		actual = type(actualError)

	assert actual == expected, uniformTestFailureMessage(messageExpected, messageActual, functionTarget.__name__, *arguments, **keywordArguments)  # ty:ignore[unresolved-attribute]
