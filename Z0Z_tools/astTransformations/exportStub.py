# ruff: noqa: D100
from __future__ import annotations

from astToolkit import Be, Grab, Make, NodeChanger, parseLogicalPath2astModule, Then
from astToolkit.containers import LedgerOfImports
from astToolkit.transformationTools import makeDictionaryFunctionDef, write_astModule
from typing import TYPE_CHECKING
from Z0Z_tools import DOTitems, DOTvalues
import ast

if TYPE_CHECKING:
    from hunterMakesPy import identifierDotAttribute

identifierPackage: str = 'humpy_toolz'
logicalPath: identifierDotAttribute = f'{identifierPackage}.functoolz'
astModule: ast.Module = parseLogicalPath2astModule(logicalPath)

ledger = LedgerOfImports(astModule)

NodeChanger(Be.FunctionDef, Grab.bodyAttribute(Then.replaceWith([Make.Constant(...)]))).visit(astModule)
NodeChanger(Be.Expr, Then.removeIt).visit(astModule)
print(ast.unparse(astModule))

# ff = DOTvalues(makeDictionaryFunctionDef(astModule))
# noBody = NodeChanger(Be.FunctionDef, Grab.bodyAttribute(Then.replaceWith([Make.Constant(...)]))).visit
# ff = map(noBody, ff)
# print(*map(ast.unparse, ledger.makeList_ast()), *map(ast.unparse, ff), sep='\n\n')

