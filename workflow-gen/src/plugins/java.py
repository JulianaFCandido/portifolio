"""
Plugin for detecting Java projects and generating GitHub Actions workflows.
"""

import os
from typing import Optional

from src.plugins import CIPluginInterface
from src.utils import template


class JavaPlugin(CIPluginInterface):
    def detect_language(self, project_path: str) -> Optional[str]:
        """
        Detects if the project is a Java project.
        """
        if os.path.exists(os.path.join(project_path, "pom.xml")) or os.path.exists(
            os.path.join(project_path, "build.gradle")
        ):
            return "java"
        return None

    def get_dependencies(self, project_path: str) -> dict[str, str]:
        """
        Detects the testing framework and linter used in the project.
        """
        dependencies = {"test": "junit", "linter": "checkstyle"}
        return dependencies

    def generate_workflow(self, language: str, test: str, linter: str) -> str:
        """
        Generates the content of the .github/workflows/main.yml file for Java.
        """
        context = {
            "language": language,
            "version": "3.9",
            "test": test,
            "linter": linter,
        }

        return template.render("ci_template.yml.j2", context)
