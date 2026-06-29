"""#======== Post-transformation: act on the new packages. ========"""
from __future__ import annotations

from astToolkit import Grab, IfThis, NodeChanger, NodeTourist, parsePathFilename2astModule, Then
from astToolkit.transformationTools import write_astModule
from Z0Z_tools.astTransformations._theSSOT import regexChangeImports, settingsFor, settingsWrite_astModule
from hunterMakesPy import raiseIfNone
from hunterMakesPy.filesystemToolkit import writeStringToHere
from typing import TYPE_CHECKING

if TYPE_CHECKING:
	from pathlib import Path
	import ast

def makeStatic__version__() -> None:  # noqa: D103
	# NOTE Static version to replace the dynamic version so it passes the tests from the original packages.
	astAssign__toolz_version__: ast.Assign = raiseIfNone(NodeTourist(IfThis.isAssignAndTargets0Is(IfThis.isNameIdentifier('__toolz_version__')), Then.extractIt).captureLastMatch(parsePathFilename2astModule(settingsFor['humpy_cytoolz'].pathPackage / '__init__.py')))
	NodeChanger(IfThis.isNameIdentifier('__toolz_version__'), Grab.idAttribute(Then.replaceWith('__version__'))).visit(astAssign__toolz_version__)
	for aPackage in ('humpy_cytoolz', 'humpy_toolz'):
		pathFilename__init__: Path = settingsFor[aPackage].pathPackage / '__init__.py'
		astModule: ast.Module = parsePathFilename2astModule(pathFilename__init__)
		astModule.body.insert(5, astAssign__toolz_version__)
		write_astModule(astModule, pathFilename__init__, settingsWrite_astModule)

	# NOTE Find and replace a handful of textual references to the original packages.
		for pathFilename in pathFilename__init__.parent.rglob(f"*{settingsFor[aPackage].fileExtension}"):
			writeStringToHere(regexChangeImports(pathFilename.read_text()), pathFilename)

if __name__ == '__main__':
	makeStatic__version__()

r"""More WTF
(.venv) C:\apps\hunterMakesPy>py assimilate\refine_humpy.py
Traceback (most recent call last):
  File "C:\apps\hunterMakesPy\assimilate\refine_humpy.py", line 2, in <module>
    from assimilate import regexChangeImports, settingsFor, settingsWrite_astModule
ModuleNotFoundError: No module named 'assimilate'

(.venv) C:\apps\hunterMakesPy>py
Python 3.14.3 (tags/v3.14.3:323c59a, Feb  3 2026, 16:04:56) [MSC v.1944 64 bit (AMD64)] on win32
Type "help", "copyright", "credits" or "license" for more information.
Ctrl click to launch VS Code Native REPL
>>> from assimilate.refine_humpy import makeStatic__version__
>>> makeStatic__version__()
>>>
"""
