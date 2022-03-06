import pkgutil
import subprocess
import sys
from importlib import import_module
from types import ModuleType
from typing import List, Optional

from interactions.ext import Base, Version, __path__ as ext_path


class ExtData:
    """
    A class representing data from an extension

    :ivar ModuleType ext: The python module of the ext
    :ivar str name: The name of the module
    :ivar Optional[Version] version: The Version of the module
    :ivar Optional[Base] base: The Base of the module
    """
    def __init__(self, ext: ModuleType):
        """
        :param ext: The module to gather data from
        :type ext: ModuleType
        """
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
    """
    Installs a ext through pip using its full path

    :param name: The name of the package
    :type name: str
    """
    subprocess.check_call([sys.executable, "-m", "pip", "install", name])
    # todo figure out how to return object?


def get_exts() -> List[ExtData]:
    """
    Get all currently installed exts

    :return: A list of the currently installed exts
    :rtype: List[ExtData]
    """
    modules = [
        mod
        for mod in pkgutil.iter_modules(
            ext_path, prefix="interactions.ext."
        )
        if mod.ispkg
    ]

    return [ExtData(import_module(mod.name)) for mod in modules]


def get_ext(name: str) -> ExtData:
    """
    Get an extension by name

    :param name: The name of the extension
    :type name: str
    :return: The extension
    :rtype: ExtData
    """
    module = next(
        filter(
            lambda data: data.name == name,
            pkgutil.iter_modules(ext_path),
        ),
        None,
    )

    return ExtData(import_module(f"interactions.ext.{module.name}"))


# what do I need to do?
# - Docs
# - list installed exts
# - auto setup() exts [Done in Toolbox, but needs to take custom args]
# - check if item is in any ext (services) [Done in toolbox]
# - be able to run as main
# - - view ext info (version, description, etc.)

# Rules as to what needs to be in a module:
# - The module MUST be under interactions.ext
# - The setup function SHOULD be repeatable
# - The module SHOULD have a Base
# - The module CAN have a version
