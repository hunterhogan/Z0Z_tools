# ruff: noqa: D100
from astToolkit import Be, Grab, Make, NodeChanger, parseLogicalPath2astModule, Then
from astToolkit.transformationTools import write_astModule
from hunterMakesPy import identifierDotAttribute
import ast

identifierPackage: str = 'humpy_toolz'
logicalPath: identifierDotAttribute = f'{identifierPackage}.dicttoolz'
astModule: ast.Module = parseLogicalPath2astModule(logicalPath)

NodeChanger(Be.FunctionDef, Grab.bodyAttribute(Then.replaceWith([Make.Constant(...)]))).visit(astModule)
NodeChanger(Be.Expr, Then.removeIt).visit(astModule)

print(ast.unparse(astModule))
