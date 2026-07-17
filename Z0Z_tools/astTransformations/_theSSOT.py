from __future__ import annotations

from functools import partial
from hunterMakesPy import identifierDotAttribute, PackageSettings
from hunterMakesPy.filesystemToolkit import settings_autoflakeDEFAULT, settings_isortDEFAULT
from pathlib import Path
from typing import Any
import re as regex

"""# DEVELOPMENT
1. Reconcile logic differences between toolz and cytoolz.
2. Initiate changes from toolz because I know Python, not Cython.
3. Use `astToolkit` to automate changes propagating from toolz to cytoolz.
4. Switch to `optype` to enable sophisticated type annotations.
5. `optype` Python>=3.12, so switch to Python>=3.12.
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
"""# The original plan, 2026 March 22:
noticeCopyrightHeader: str = textwrap.fill("Some of the original or derivative works in this directory and its subdirectories may be protected by the following copyright.", width=80) + "\n___\n\n"
	settingsFor[humpyPackage].pathPackage.mkdir(parents=True, exist_ok=True)

	if identifierTransformee == 'tlz':
		pathTransformee = Path(f'/clones/toolz/{identifierTransformee}')
	else:
		writeStringToHere(noticeCopyrightHeader + (pathTransformee.parent / 'LICENSE.txt').read_text(encoding='utf-8'), settingsFor[humpyPackage].pathPackage / 'Notice_of_Copyright.txt')

	transformALLdot_pyHere.append((pathTransformee, identifierTransformee, getOtherName[identifierTransformee]))

My goal is to feed changes back to the original source via a pull request. If the source updates, pull
the update, and the cycle continues. See, e.g., https://github.com/pytoolz/toolz/issues/622

2026 July 3: I'm proceeding under the assumption that the original plan is not viable.

Original sources would each have their own git branch.
- https://github.com/pytoolz/toolz/
- https://github.com/pytoolz/cytoolz/
- https://github.com/mgrinshpon/toolz-stubs

On their branch, they are processed through the chop shop. Desired changes are moved from the branch
to main by a pull request. If the sources do not change, the branch will stay unchanged, but main can
improve.
"""
