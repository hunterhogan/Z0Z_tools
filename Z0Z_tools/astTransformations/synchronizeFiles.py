# ruff: noqa D100, D103
from __future__ import annotations

from astToolkit import Be, Grab, NodeChanger, parsePathFilename2astModule
from astToolkit.transformationTools import write_astModule
from collections import deque
from functools import partial, reduce
from hunterMakesPy import raiseIfNone
from hunterMakesPy.filesystemToolkit import writeStringToHere
from pathlib import Path
from typing import TYPE_CHECKING
from Z0Z_tools.astTransformations._theSSOT import settingsFor, settingsWrite_astModule
import ast
import re as regex

if TYPE_CHECKING:
	from collections.abc import Callable, Iterable, Mapping
	from hunterMakesPy import PackageSettings
	from typing_extensions import TypeIs

def strStartsWith(identifierPackage: str) -> Callable[[str | None], TypeIs[str]]:
	def workhorse(node: str | None) -> TypeIs[str]:
		return isinstance(node, str) and (node.startswith(identifierPackage))
	return workhorse

def synchronizeFilesTests(settingsPackageSource: PackageSettings, settingsPackageDuplicate: PackageSettings, listFilenames: Iterable[str] = frozenset(), relativePathTests: Path = Path('tests')) -> None:
	for filename in listFilenames:
		astModule: ast.Module = parsePathFilename2astModule(settingsPackageSource.pathPackage / relativePathTests / filename)

		NodeChanger(
			Be.ImportFrom.moduleIs(strStartsWith(settingsPackageSource.identifierPackage))
			, Grab.moduleAttribute(lambda node: raiseIfNone(node).replace(settingsPackageSource.identifierPackage, settingsPackageDuplicate.identifierPackage, 1))
		).visit(astModule)

		write_astModule(astModule, settingsPackageDuplicate.pathPackage / relativePathTests / filename, settingsWrite_astModule)

#==== Everything below this line is incompetent AI dogshit and needs to be rewritten. ====

PythonDocstringNode = ast.AsyncFunctionDef | ast.ClassDef | ast.FunctionDef

matchCythonDefinition = regex.compile(
	r"^(?:def\s+|cpdef\s+(?:[A-Za-z_]\w*\s+)*)(?P<function>[A-Za-z_]\w*)\s*\("
	r"|^(?:cdef\s+class\s+|class\s+)(?P<class>[A-Za-z_]\w*)\b"
)
matchDocstringStart = regex.compile(r"^[ \t]*(?:[rRuUbB]{0,4})?(?P<quote>'''|\"\"\")")

def convertDocstringForDuplicatePackage(docstring: str, settingsPackageSource: PackageSettings, settingsPackageDuplicate: PackageSettings) -> str:
	return (
		docstring
		.replace(settingsPackageSource.identifierPackage, settingsPackageDuplicate.identifierPackage)
		.replace('dictcytoolz', 'dicttoolz')
		.replace('funccytoolz', 'functoolz')
		.replace('itercytoolz', 'itertoolz')
		.replace('cytoolz.readthedocs', 'toolz.readthedocs')
	)

def getDocstringItem(node: ast.AST, settingsPackageSource: PackageSettings, settingsPackageDuplicate: PackageSettings) -> tuple[str, str] | None:
	if not isinstance(node, PythonDocstringNode):
		return None
	docstring = ast.get_docstring(node, clean=False)
	if docstring is None:
		return None
	return node.name, convertDocstringForDuplicatePackage(docstring, settingsPackageSource, settingsPackageDuplicate)

def getDocstringsByIdentifier(pathFilename: Path, settingsPackageSource: PackageSettings, settingsPackageDuplicate: PackageSettings) -> Mapping[str, str]:
	return dict(filter(None, map(partial(getDocstringItem, settingsPackageSource=settingsPackageSource, settingsPackageDuplicate=settingsPackageDuplicate), ast.parse(pathFilename.read_text(encoding='utf-8')).body)))

def getPathFilenameWithExtension(settingsPackage: PackageSettings, filename: str, fileExtension: str) -> Path:
	return settingsPackage.pathPackage / Path(filename).with_suffix(fileExtension)

def getLineIndent(line: str) -> str:
	return line[:len(line) - len(line.lstrip(' \t'))]

def getCythonDefinitionName(line: str) -> str | None:
	matchDefinition = matchCythonDefinition.match(line)
	if matchDefinition is None:
		return None
	return matchDefinition.group('function') or matchDefinition.group('class')

def findCythonDefinitionLine(listLines: list[str], identifier: str) -> int | None:
	indexLine: int = 0
	indexLineDefinition: int | None = None
	while indexLine < len(listLines) and indexLineDefinition is None:
		if getCythonDefinitionName(listLines[indexLine]) == identifier:
			indexLineDefinition = indexLine
		indexLine += 1
	return indexLineDefinition

def findCythonHeaderEndLine(listLines: list[str], indexLineDefinition: int, identifier: str) -> int:
	indexLine: int = indexLineDefinition
	while indexLine < len(listLines) and not listLines[indexLine].rstrip().endswith(':'):
		indexLine += 1
	if indexLine == len(listLines):
		raise ValueError(f"Could not find the end of the Cython definition header for {identifier!r}.")
	return indexLine

def findFirstCythonBodyLine(listLines: list[str], indexLineHeaderEnd: int, identifier: str) -> int:
	indexLine: int = indexLineHeaderEnd + 1
	while indexLine < len(listLines) and not listLines[indexLine].strip():
		indexLine += 1
	if indexLine == len(listLines):
		raise ValueError(f"Could not find a Cython definition body for {identifier!r}.")
	return indexLine

def findCythonDocstringEndLine(listLines: list[str], indexLineDocstringStart: int, quoteDocstring: str, identifier: str) -> int:
	indexQuoteStart: int = listLines[indexLineDocstringStart].index(quoteDocstring) + len(quoteDocstring)
	indexLine: int = indexLineDocstringStart
	if quoteDocstring not in listLines[indexLineDocstringStart][indexQuoteStart:]:
		indexLine = indexLineDocstringStart + 1
		while indexLine < len(listLines) and quoteDocstring not in listLines[indexLine]:
			indexLine += 1
		if indexLine == len(listLines):
			raise ValueError(f"Could not find the end of the Cython docstring for {identifier!r}.")
	return indexLine

def getDocstringDelimiter(docstring: str) -> str:
	if '"""' not in docstring:
		return '"""'
	if "'''" not in docstring:
		return "'''"
	raise ValueError('Cannot write a docstring that contains both triple-double and triple-single quotes.')

def formatCythonDocstring(docstring: str, indent: str) -> list[str]:
	delimiterDocstring: str = getDocstringDelimiter(docstring)
	return f"{indent}{delimiterDocstring}{docstring}{delimiterDocstring}\n".splitlines(keepends=True)

def replaceCythonDocstringForIdentifier(listLines: list[str], itemDocstring: tuple[str, str]) -> list[str]:
	identifier, docstring = itemDocstring
	indexLineDefinition = findCythonDefinitionLine(listLines, identifier)
	if indexLineDefinition is None:
		return listLines

	indexLineHeaderEnd: int = findCythonHeaderEndLine(listLines, indexLineDefinition, identifier)
	indexLineBody: int = findFirstCythonBodyLine(listLines, indexLineHeaderEnd, identifier)
	listLinesDocstring: list[str] = formatCythonDocstring(docstring, getLineIndent(listLines[indexLineBody]))
	matchExistingDocstring = matchDocstringStart.match(listLines[indexLineBody])
	if matchExistingDocstring is None:
		return listLines[:indexLineHeaderEnd + 1] + listLinesDocstring + listLines[indexLineHeaderEnd + 1:]

	indexLineDocstringEnd: int = findCythonDocstringEndLine(listLines, indexLineBody, matchExistingDocstring.group('quote'), identifier)
	return listLines[:indexLineBody] + listLinesDocstring + listLines[indexLineDocstringEnd + 1:]

def synchronizeFileDocstrings(settingsPackageSource: PackageSettings, settingsPackageDuplicate: PackageSettings, filename: str) -> None:
	pathFilenameSource: Path = getPathFilenameWithExtension(settingsPackageSource, filename, '.py')
	pathFilenameDuplicate: Path = getPathFilenameWithExtension(settingsPackageDuplicate, filename, '.pyx')
	listLines: list[str] = pathFilenameDuplicate.read_text(encoding='utf-8').splitlines(keepends=True)
	docstringsByIdentifier: Mapping[str, str] = getDocstringsByIdentifier(pathFilenameSource, settingsPackageSource, settingsPackageDuplicate)
	pathFilenameDuplicate.write_text(''.join(reduce(replaceCythonDocstringForIdentifier, docstringsByIdentifier.items(), listLines)), encoding='utf-8', newline='\n')

def synchronizeFilesDocstrings(settingsPackageSource: PackageSettings, settingsPackageDuplicate: PackageSettings, listFilenames: Iterable[str] = frozenset()) -> None:
	deque(map(partial(synchronizeFileDocstrings, settingsPackageSource, settingsPackageDuplicate), listFilenames), maxlen=0)

if __name__ == '__main__':
	listFilenames: Iterable[str] = frozenset(('test_dicttoolz.py','test_itertoolz.py',))
	synchronizeFilesTests(settingsFor['humpy_toolz'], settingsFor['humpy_cytoolz'], listFilenames)

	listFilenamesDocstrings: Iterable[str] = frozenset(('dicttoolz', 'functoolz', 'itertoolz', 'recipes', 'utils'))
	synchronizeFilesDocstrings(settingsFor['humpy_toolz'], settingsFor['humpy_cytoolz'], listFilenamesDocstrings)
