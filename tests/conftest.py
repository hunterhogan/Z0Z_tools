import os
import shutil
import uuid
from pathlib import Path
import pytest
from typing import Generator, Set, Dict

# SSOT for test data paths
pathDataSamples = Path("tests/dataSamples")
pathTempRoot = pathDataSamples / "tmp"

# The registrar maintains the register of temp files
registrarTempFiles: Set[Path] = set()

def addTempFileToRegister(path: Path) -> None:
    """The registrar adds a temp file to the register."""
    registrarTempFiles.add(path)

def cleanupTempFileRegister() -> None:
    """The registrar cleans up temp files in the register."""
    for pathTemp in sorted(registrarTempFiles, reverse=True):
        try:
            if pathTemp.is_file():
                pathTemp.unlink(missing_ok=True)
            elif pathTemp.is_dir():
                shutil.rmtree(pathTemp, ignore_errors=True)
        except Exception as ERRORmessage:
            print(f"Warning: Failed to clean up {pathTemp}: {ERRORmessage}")
    registrarTempFiles.clear()

@pytest.fixture(scope="session", autouse=True)
def setupTeardownTestData() -> Generator[None, None, None]:
    """Auto-fixture to setup test data directories and cleanup after."""
    pathDataSamples.mkdir(exist_ok=True)
    pathTempRoot.mkdir(exist_ok=True)
    yield
    cleanupTempFileRegister()

@pytest.fixture
def pathTempTesting(request) -> Path:
    """Create a unique temp directory for each test function."""
    # Sanitize test name for filesystem compatibility
    sanitizedName = request.node.name.replace('[', '_').replace(']', '_').replace('/', '_')
    uniqueDirectory = f"{sanitizedName}_{uuid.uuid4()}"
    pathTemp = pathTempRoot / uniqueDirectory
    pathTemp.mkdir(parents=True)

    addTempFileToRegister(pathTemp)
    return pathTemp

@pytest.fixture
def redirectPipAnything(monkeypatch, pathTempTesting) -> None:
    """Redirect pip package operations to test directories."""
    def mockTempdir(*args, **kwargs) -> str:
        pathTemp = pathTempTesting / f"pip_temp_{uuid.uuid4()}"
        pathTemp.mkdir(parents=True)
        addTempFileToRegister(pathTemp)
        return str(pathTemp)

    monkeypatch.setattr('tempfile.mkdtemp', mockTempdir)
    monkeypatch.setattr('tempfile.gettempdir', lambda: str(pathTempTesting))
