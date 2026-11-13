"""Hooks that name the compiled modules under test, so a stale or unexpected build is visible before anyone reads a failure as a defect."""
from __future__ import annotations

from datetime import datetime
from functools import partial
from hunterMakesPy import raiseIfNone
from pathlib import Path
from typing import TYPE_CHECKING
import humpy_cytoolz.dicttoolz
import humpy_cytoolz.functoolz
import humpy_cytoolz.itertoolz
import humpy_cytoolz.recipes
import humpy_cytoolz.utils

if TYPE_CHECKING:
	from types import ModuleType
	import pytest

boxOfModulesCompiled: tuple[ModuleType, ...] = (
	humpy_cytoolz.dicttoolz, humpy_cytoolz.functoolz, humpy_cytoolz.itertoolz, humpy_cytoolz.recipes, humpy_cytoolz.utils)

def getPathFilenameCompiled(module: ModuleType) -> Path:
	"""Return the file that the import system loaded for `module`."""
	return Path(raiseIfNone(raiseIfNone(module.__spec__).origin))

def getPathFilenameSource(module: ModuleType) -> Path:
	"""Return the `.pyx` file beside the file that the import system loaded for `module`."""
	return getPathFilenameCompiled(module).with_name(f"{module.__name__.rpartition('.')[2]}.pyx")

def describeModuleCompiled(module: ModuleType) -> str:
	"""Name the file loaded for `module`, when it was built, and when its `.pyx` source last changed."""
	return (f'{module.__name__}: {getPathFilenameCompiled(module)} built {datetime.fromtimestamp(getPathFilenameCompiled(module).stat().st_mtime):%Y-%m-%d %H:%M:%S}'
		f'; {getPathFilenameSource(module).name} changed {datetime.fromtimestamp(getPathFilenameSource(module).stat().st_mtime):%Y-%m-%d %H:%M:%S}')

def sourceChangedAfterBuild吗(pathRoot: Path, module: ModuleType) -> bool:
	"""Whether `module` was built in the working tree under `pathRoot` before its `.pyx` source last changed.

	An installed distribution is never stale by this measure: installation sets the times of its files, so their order says
	nothing about the build.
	"""
	return pathRoot in getPathFilenameCompiled(module).parents and getPathFilenameCompiled(module).stat().st_mtime < getPathFilenameSource(module).stat().st_mtime

def pytest_report_header(config: pytest.Config) -> list[str]:
	"""Describe each compiled module of `humpy_cytoolz` at the top of the session."""
	return [*map(describeModuleCompiled, boxOfModulesCompiled)]

def pytest_terminal_summary(terminalreporter: pytest.TerminalReporter, exitstatus: int, config: pytest.Config) -> None:
	"""After the results, even with `-q`, name each compiled module that is older than its `.pyx` source."""
	boxOfModulesStale: list[ModuleType] = [*filter(partial(sourceChangedAfterBuild吗, config.rootpath), boxOfModulesCompiled)]
	if boxOfModulesStale:
		terminalreporter.write_sep('=', 'compiled modules older than their source: rebuild before reading these results as defects', red=True)
		terminalreporter.write_line('\n'.join(map(describeModuleCompiled, boxOfModulesStale)))
