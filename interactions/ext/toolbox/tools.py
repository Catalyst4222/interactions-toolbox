from typing import Dict

from interactions import Client

from .installer import ExtData, get_ext


class Tools:
    def __init__(self, client: Client):
        self.client = client

        self.extensions: Dict[str, ExtData] = {}
        self.tools: Dict[str, ...] = {}

    def __getattribute__(self, item):
        try:
            return super().__getattribute__(item)
        except AttributeError:
            if item in self.tools:
                return self.tools[item]
            raise

    def add(self, item: str, ext: str):
        """Add a new item to your toolbox"""
        if item in self.tools:
            raise ValueError(f"{item} is already loaded as a tool!")

        ext_: ExtData = self._get_ext(ext)

        service = ext_.base.services.get(item)
        if service is None:
            raise ValueError(f"The {item} service was not found!")

        self.tools[item] = service
        return service

    def _get_ext(self, ext: str) -> ExtData:
        """Get an ext, and load it if not found"""
        if ext not in self.extensions:
            ext_ = self.extensions[ext] = get_ext(ext)
            if hasattr(ext_.ext, "setup"):
                ext_.ext.setup(self.client)

        return self.extensions[ext]
