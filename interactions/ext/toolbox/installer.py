import pkgutil
import subprocess
import sys
from importlib import import_module
from types import ModuleType
from typing import Dict, List, Optional, TypedDict

import interactions.ext
from interactions.ext import Base, Version

rules = """
The ext must be a package (no single files allowed)
Must have `version` be a ext.Version
must have `base` be a ext.Base 
"""


class ExtData:
    def __init__(self, ext: ModuleType):
        self.ext: ModuleType = ext
        self.name: str = ext.__name__

        if hasattr(ext, "version"):
            self.version: Optional[Version] = ext.version
        elif hasattr(ext, "__version__"):
            self.version: Optional[Version] = Version(version=ext.__version__)
        else:
            self.version: Optional[Version] = None

        self.base: Base = ext.base if hasattr(ext, "base") else None

    def __repr__(self):
        return f"<ExtData of {self.name}>"


def install_ext(name: str):
    """Installs a ext through pip using its full path"""
    subprocess.check_call([sys.executable, "-m", "pip", "install", name])
    # todo figure out how to return object?


def get_exts() -> List[ExtData]:
    """Get all currently installed exts"""
    modules = [
        mod
        for mod in pkgutil.iter_modules(
            interactions.ext.__path__, prefix="interactions.ext."
        )
        if mod.ispkg
    ]

    return [ExtData(import_module(mod.name)) for mod in modules]


def get_ext(name: str) -> ExtData:
    module = next(
        filter(
            lambda data: data.name == name,
            pkgutil.iter_modules(interactions.ext.__path__),
        ),
        None,
    )

    return ExtData(import_module(f"interactions.ext.{module.name}"))


# what do I need to do?
# - list installed exts
# - auto setup() exts [Done in Toolbox]
# - check if item is in any ext (services) [Done in toolbox]
# - be able to run as main
# - - view ext info (version, description, etc.)
#
