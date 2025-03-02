from collections.abc import Iterable
from os import PathLike
from typing import Any

def dataTabularTOpathFilenameDelimited(pathFilename: str | PathLike[Any], tableRows: Iterable[Iterable[Any]], tableColumns: Iterable[Any], delimiterOutput: str = '\t') -> None: ...
def findRelativePath(pathSource: str | PathLike[Any], pathDestination: str | PathLike[Any]) -> str: ...
def makeDirsSafely(pathFilename: Any) -> None: ...
