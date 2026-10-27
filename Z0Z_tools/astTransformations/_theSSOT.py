from __future__ import annotations

from hunterMakesPy.filesystemToolkit import settings_autoflakeDEFAULT, settings_isortDEFAULT
from typing import Any

settingsWrite_astModule: dict[str, dict[str, Any]] = {'isort': settings_isortDEFAULT, 'autoflake': settings_autoflakeDEFAULT}
settingsWrite_astModule['autoflake']['remove_all_unused_imports'] = False
settingsWrite_astModule['autoflake']['expand_star_imports'] = False
settingsWrite_astModule['autoflake']['ignore_init_module_imports'] = True
