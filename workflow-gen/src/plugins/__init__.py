"""
Defines the interface for CI plugins and provides a class for loading plugins.
"""

import inspect
import importlib
from pathlib import Path
from typing import Optional, Dict

from src.utils import i18n


class CIPluginInterface:
    """
    Interface for CI plugins.
    """

    def detect_language(self, project_path: str) -> Optional[str]:
        """
        Detects the programming language of the project.
        """
        raise NotImplementedError

    def get_dependencies(self, project_path: str) -> Dict[str, str]:
        """
        Detects the testing framework and linter used in the project.
        """
        raise NotImplementedError

    def generate_workflow(self, language: str, test: str, linter: str) -> str:
        """
        Generates the content of the .github/workflows/main.yml file.
        """
        raise NotImplementedError


class PluginLoader:
    """
    Loads CI plugins from a directory.
    """

    def __init__(self, plugin_dir: str = "src/plugins"):
        self.plugin_dir = plugin_dir

    def load_plugins(self) -> Dict[str, CIPluginInterface]:
        """
        Loads plugins from the specified directory.
        """
        plugins: Dict[str, CIPluginInterface] = {}
        plugin_path = Path(self.plugin_dir)
        for filepath in plugin_path.glob("*.py"):
            if filepath.name == "__init__.py":
                continue

            module_name = filepath.stem
            module_path = f"{__package__}.{module_name}"
            try:
                module = importlib.import_module(module_path)
                for name, obj in inspect.getmembers(module):
                    if inspect.isclass(obj) and issubclass(obj, CIPluginInterface):
                        plugin_class = getattr(module, name)
                        plugins[module_name] = plugin_class
            except Exception as e:
                print(i18n.get_message("errors", "plugin_error", plugin_name=module_name, error=e))
        return plugins
