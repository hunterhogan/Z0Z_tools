# ruff:file-ignore[undocumented-public-module, undocumented-public-function]
from __future__ import annotations

from astToolkit import Be, Grab, IfThis, Make, NodeChanger, parsePathFilename2astModule, Then
from astToolkit.containers import LedgerOfImports
from astToolkit.transformationTools import write_astModule
from copy import deepcopy
from functools import partial
from pathlib import Path
from typing import TYPE_CHECKING
from Z0Z_tools.astTransformations._theSSOT import settingsWrite_astModule

if TYPE_CHECKING:
	from collections.abc import Iterable
	from hunterMakesPy import PackageSettings
	from typing_extensions import TypeIs
	import ast

def annotatedAssignmentValueIsReplaceable(node: ast.AST) -> TypeIs[ast.AnnAssign]:
	return (
		Be.AnnAssign(node)
		and not Be.AnnAssign.targetIs(IfThis.isNameIdentifier('__all__'))(node)
		and not Be.AnnAssign.annotationIs(
			IfThis.isAnyOf(IfThis.isNestedNameIdentifier('Final'), IfThis.isNestedNameIdentifier('TypeAlias'))
		)(node)
	)

def assignmentIsReplaceable(node: ast.AST) -> TypeIs[ast.Assign]:
	return Be.Assign(node) and not IfThis.isAssignAndTargets0Is(IfThis.isNameIdentifier('__all__'))(node)

def exportStub(settingsPackageSource: PackageSettings, settingsPackageDuplicate: PackageSettings, filename: str) -> Path:
	astModule: ast.Module = parsePathFilename2astModule(settingsPackageSource.pathPackage / Path(filename).with_suffix('.py'))

	NodeChanger(Be.Expr, Then.removeIt).visit(astModule)

	ellipsisBody: list[ast.stmt] = [Make.Expr(Make.Constant(...))]
	NodeChanger(Be.FunctionDef, Grab.bodyAttribute(Then.replaceWith(ellipsisBody))).visit(astModule)
	NodeChanger(Be.AsyncFunctionDef, Grab.bodyAttribute(Then.replaceWith(ellipsisBody))).visit(astModule)

	ledgerOfImports = LedgerOfImports(astModule)
	NodeChanger(IfThis.isAnyOf(Be.Import, Be.ImportFrom), Then.removeIt).visit(astModule)
	NodeChanger(Be.If, Then.removeIt).visit(astModule)

	NodeChanger(assignmentIsReplaceable, Then.removeIt).visit(astModule)
	NodeChanger(annotatedAssignmentValueIsReplaceable, Grab.valueAttribute(Then.replaceWith(None))).visit(astModule)
	NodeChanger(Be.ClassDef, Grab.bodyAttribute(Then.replaceWith(ellipsisBody))).visit(astModule)

	Grab.bodyAttribute(lambda listStatements: [*ledgerOfImports.makeList_ast(), *listStatements])(astModule)

	settingsWriteStub_astModule = deepcopy(settingsWrite_astModule)
	settingsWriteStub_astModule['autoflake']['ignore_init_module_imports'] = False
	settingsWriteStub_astModule['autoflake']['remove_all_unused_imports'] = True
	return write_astModule(
		astModule,
		settingsPackageDuplicate.pathPackage / Path(filename).with_suffix('.pyi'),
		settingsWriteStub_astModule,
	)

def exportStubs(
	settingsPackageSource: PackageSettings,
	settingsPackageDuplicate: PackageSettings,
	listFilenames: Iterable[str] = frozenset(),
) -> tuple[Path, ...]:
	return tuple(map(partial(exportStub, settingsPackageSource, settingsPackageDuplicate), listFilenames))
