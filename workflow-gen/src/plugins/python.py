"""
Plugin for detecting Python projects and generating GitHub Actions workflows.
"""

import os
from typing import Optional

from src.plugins import CIPluginInterface
from src.utils import template


class PythonPlugin(CIPluginInterface):
    def detect_language(self, project_path: str) -> Optional[str]:
        """
        Detects if the project is a Python project.
        """
        requirements_path = os.path.join(project_path, "requirements.txt")
        setup_path = os.path.join(project_path, "setup.py")
        if os.path.exists(requirements_path) or os.path.exists(setup_path):
            return "python"
        return None

    def get_dependencies(self, project_path: str) -> dict[str, str]:
        """
        Detects the testing framework and linter used in the project.
        """
        dependencies = {"test": None, "linter": None}
        if os.path.exists(os.path.join(project_path, "requirements.txt")):
            with open(os.path.join(project_path, "requirements.txt"), "r", encoding="utf-8") as f:
                for line in f:
                    if "pytest" in line:
                        dependencies["test"] = "pytest"
                    if "flake8" in line:
                        dependencies["linter"] = "flake8"
                    if "pylint" in line:
                        dependencies["linter"] = "pylint"
        return dependencies

    def generate_workflow(self, language: str, test: str, linter: str) -> str:
        """
        Generates the content of the .github/workflows/main.yml file for Python.
        """
        context = {
            "language": language,
            "version": "3.9",
            "test": test,
            "linter": linter,
        }

        return template.render("ci_template.yml.j2", context)
