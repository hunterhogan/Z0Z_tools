# ruff: noqa: D103
"""Ingest external packages and files."""
from __future__ import annotations

from astToolkit import Be, Grab, IfThis, Make, NodeChanger, parsePathFilename2astModule, Then
from astToolkit.transformationTools import write_astModule
from functools import partial
from hunterMakesPy.filesystemToolkit import writeStringToHere
from itertools import product as CartesianProduct
from operator import contains, eq as equalTo
from shutil import copytree
from typing import cast, TYPE_CHECKING
from Z0Z_tools.astTransformations._theSSOT import (
	allTransformeePackages, cythonDirectives, getOtherName, pathRoot_toolz_stubs, regexChangeImports, settingsFor, settingsWrite_astModule,
	subModules, transformALLdot_pyHere)
import sys

if TYPE_CHECKING:
	from hunterMakesPy import identifierDotAttribute
	import ast

if sys.version_info < (3, 12):
	message = f"Python 3.12 or higher is required, but you are using {sys.version_info.major}.{sys.version_info.minor}."
	raise RuntimeError(message)

def transformPackages() -> None:

	for pathTransformee, identifierTransformee, humpyPackage in transformALLdot_pyHere:
		for pathRoot, listDirectories, listFilenames in pathTransformee.walk():
			if '__pycache__' in listDirectories:
				listDirectories.remove('__pycache__')
			for directory in listDirectories:
				(settingsFor[humpyPackage].pathPackage / directory).mkdir(parents=True, exist_ok=True)

			for filename in filter(lambda filename: filename.endswith(settingsFor[humpyPackage].fileExtension), listFilenames):
				astModule: ast.Module = parsePathFilename2astModule(pathRoot / filename)

				for packageTransformee, identifierModule in CartesianProduct(allTransformeePackages, subModules):
					changeImportFrom = NodeChanger(Be.ImportFrom.moduleIs(partial(equalTo, packageTransformee + identifierModule)), Grab.moduleAttribute(Then.replaceWith(getOtherName[packageTransformee] + identifierModule)))
					changeImportFrom.visit(astModule)

					changeImport = NodeChanger(Be.alias.nameIs(partial(equalTo, packageTransformee + identifierModule)), Grab.nameAttribute(Then.replaceWith(getOtherName[packageTransformee] + identifierModule)))
					changeImport.visit(astModule)

					changeConstant = NodeChanger(IfThis.isConstant_value(packageTransformee + identifierModule), Then.replaceWith(Make.Constant(getOtherName[packageTransformee] + identifierModule)))
					changeConstant.visit(astModule)

					if not identifierModule:
						stringOld: identifierDotAttribute = f" {packageTransformee}{identifierModule}"
						changeIdentifierInConstant = NodeChanger(IfThis.isAllOf(Be.Constant.valueIs(lambda nodeDOTvalue: isinstance(nodeDOTvalue, str)), Be.Constant.valueIs(lambda nodeDOTvalue, stringOld=stringOld: contains(nodeDOTvalue, stringOld))), lambda node, stringOld=stringOld, packageTransformee=packageTransformee, identifierModule=identifierModule: Make.Constant(cast('str', node.value).replace(stringOld, f" {getOtherName[packageTransformee]}{identifierModule}")))
						changeIdentifierInConstant.visit(astModule)

					else:
						stringOld: str = f"`{packageTransformee}`"
						changeBacktickIdentifierInConstant = NodeChanger(IfThis.isAllOf(Be.Constant.valueIs(lambda nodeDOTvalue: isinstance(nodeDOTvalue, str)), Be.Constant.valueIs(lambda nodeDOTvalue, stringOld=stringOld: contains(nodeDOTvalue, stringOld))), lambda node, stringOld=stringOld, packageTransformee=packageTransformee: Make.Constant(cast('str', node.value).replace(stringOld, f"`{getOtherName[packageTransformee]}`")))
						changeBacktickIdentifierInConstant.visit(astModule)

						changeName = NodeChanger(IfThis.isNameIdentifier(packageTransformee), Grab.idAttribute(Then.replaceWith(getOtherName[packageTransformee])))
						changeName.visit(astModule)

				write_astModule(astModule, settingsFor[humpyPackage].pathPackage / pathRoot.relative_to(pathTransformee) / filename, settingsWrite_astModule)

		if identifierTransformee == 'cytoolz':
			for pathFilename in pathTransformee.glob('*.pxd'):
				writeStringToHere(regexChangeImports(pathFilename.read_text()), settingsFor[humpyPackage].pathPackage / pathFilename.relative_to(pathTransformee))
			for pathFilename in pathTransformee.glob('*.pyx'):
				writeStringToHere(cythonDirectives + regexChangeImports(pathFilename.read_text().replace(identifierTransformee, getOtherName[identifierTransformee])), settingsFor[humpyPackage].pathPackage / pathFilename.relative_to(pathTransformee))

def copy_toolz_stubs() -> None:
	copytree(pathRoot_toolz_stubs, settingsFor['humpy_toolz'].pathPackage, dirs_exist_ok=True)

if __name__ == '__main__':
	transformPackages()
	copy_toolz_stubs()
