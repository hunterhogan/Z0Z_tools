from __future__ import annotations

from functools import partial
from hunterMakesPy import identifierDotAttribute, PackageSettings
from hunterMakesPy.filesystemToolkit import settings_autoflakeDEFAULT, settings_isortDEFAULT, writeStringToHere
from pathlib import Path
from typing import Any
import re as regex
import textwrap

"""# DEVELOPMENT
Potentially dynamic sources each have their own git branch.
	https://github.com/pytoolz/toolz/
	https://github.com/pytoolz/cytoolz/
	https://github.com/mgrinshpon/toolz-stubs
	On their branch, they are processed through the chop shop.
	Desired changes are moved from the branch to main by a pull request.
	If the sources do not change, the branch will stay unchanged, but main can improve.
	My goal is to feed the changes in main back to the original source via a pull request. If the source updates, then the cycle continues.

	https://github.com/getzze/toolz/tree/typed is static.
	Instead of trying to consolidate all of the changes at one time, I will process the changes per function.

Consolidate settings.
"""
#============ Eliminate hardcoding. ===============

subModulesHARDCODED: frozenset[identifierDotAttribute] = frozenset(('', '._signatures', '.compatibility', '.curried', '.curried.exceptions'
	, '.curried.operator', '.dicttoolz', '.functoolz', '.itertoolz', '.recipes', '.sandbox', '.sandbox.core', '.sandbox.parallel', '.utils'))

#============ Containers of settings. ============

settingsWrite_astModule: dict[str, dict[str, Any]] = {'isort': settings_isortDEFAULT, 'autoflake': settings_autoflakeDEFAULT}
allTransformeePackages: tuple[str, ...] = ('toolz', 'tlz', 'cytoolz')
getOtherName: dict[str, str] = {}
transformALLdot_pyHere: list[tuple[Path, str, str]] = []
settingsFor: dict[str, PackageSettings] = {}

#============ Settings without containers. ============

cythonDirectives: str = """# cython: embedsignature=True
# cython: freethreading_compatible=True
# cython: language_level=3
"""
noticeCopyrightHeader: str = textwrap.fill("Some of the original or derivative works in this directory and its subdirectories may be protected by the following copyright.", width=80) + "\n___\n\n"
pathRoot_toolz_stubs = Path("/clones/toolz-stubs/src/toolz-stubs")
regexChangeImports: partial[str] = partial(regex.sub, "(from |import )(.?.?toolz)", "\\1humpy_\\2")
subModules: frozenset[identifierDotAttribute] = subModulesHARDCODED

#============ Put settings in the containers. ============

settingsWrite_astModule['autoflake']['remove_all_unused_imports'] = False
settingsWrite_astModule['autoflake']['expand_star_imports'] = False
settingsWrite_astModule['autoflake']['ignore_init_module_imports'] = True
pathPackageRoot: Path = Path(__file__).resolve().parent.parent.parent

for identifierTransformee in allTransformeePackages:
	humpyPackage: str = f"humpy_{identifierTransformee}"
	getOtherName[identifierTransformee] = humpyPackage
	getOtherName[humpyPackage] = identifierTransformee

	pathTransformee: Path = Path(f'/clones/{identifierTransformee}/{identifierTransformee}')

	settingsFor[humpyPackage] = PackageSettings(identifierPackage=humpyPackage, pathPackage=(pathPackageRoot / humpyPackage))
	settingsFor[humpyPackage].pathPackage.mkdir(parents=True, exist_ok=True)

	if identifierTransformee == 'tlz':
		pathTransformee = Path(f'/clones/toolz/{identifierTransformee}')
	else:
		writeStringToHere(noticeCopyrightHeader + (pathTransformee.parent / 'LICENSE.txt').read_text(encoding='utf-8'), settingsFor[humpyPackage].pathPackage / 'Notice_of_Copyright.txt')

	transformALLdot_pyHere.append((pathTransformee, identifierTransformee, getOtherName[identifierTransformee]))
