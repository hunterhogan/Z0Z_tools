# ruff:file-ignore[undocumented-public-module, undocumented-public-function]
from __future__ import annotations

from astToolkit import Be, Grab, NodeChanger, parsePathFilename2astModule
from astToolkit.transformationTools import write_astModule
from hunterMakesPy import raiseIfNone
from pathlib import Path
from typing import TYPE_CHECKING
from Z0Z_tools.astTransformations._synchronizeDocstrings import synchronizeDocstrings
from Z0Z_tools.astTransformations._theSSOT import settingsFor, settingsWrite_astModule
from Z0Z_tools.astTransformations.exportStub import exportStubs

if TYPE_CHECKING:
	from collections.abc import Callable, Iterable
	from hunterMakesPy import PackageSettings
	from typing_extensions import TypeIs
	import ast

def strStartsWith(identifierPackage: str) -> Callable[[str | None], TypeIs[str]]:
	def workhorse(node: str | None) -> TypeIs[str]:
		return isinstance(node, str) and (node.startswith(identifierPackage))
	return workhorse

def synchronizeTests(settingsPackageSource: PackageSettings, settingsPackageDuplicate: PackageSettings, listFilenames: Iterable[str] = frozenset(), relativePathTests: Path = Path('tests')) -> None:
	for filename in listFilenames:
		astModule: ast.Module = parsePathFilename2astModule(settingsPackageSource.pathPackage / relativePathTests / filename)

		NodeChanger(
			Be.ImportFrom.moduleIs(strStartsWith(settingsPackageSource.identifierPackage))
			, Grab.moduleAttribute(lambda node: raiseIfNone(node).replace(settingsPackageSource.identifierPackage, settingsPackageDuplicate.identifierPackage, 1))
		).visit(astModule)

		write_astModule(astModule, settingsPackageDuplicate.pathPackage / relativePathTests / filename, settingsWrite_astModule)

if __name__ == '__main__':
	listFilenames: Iterable[str] = frozenset(('test_dicttoolz.py', 'test_itertoolz.py'))
	synchronizeTests(settingsFor['humpy_toolz'], settingsFor['humpy_cytoolz'], listFilenames)

	listFilenamesDocstrings: Iterable[str] = frozenset(('dicttoolz', 'functoolz', 'itertoolz', 'recipes', 'utils'))
	synchronizeDocstrings(settingsFor['humpy_toolz'], settingsFor['humpy_cytoolz'], listFilenamesDocstrings)
	exportStubs(settingsFor['humpy_toolz'], settingsFor['humpy_cytoolz'], listFilenamesDocstrings)
