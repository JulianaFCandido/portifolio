"""
Plugin for detecting Node.js projects and generating GitHub Actions workflows.
"""

import os
from typing import Optional
import json

from src.plugins import CIPluginInterface
from src.utils import i18n, template


class NodejsPlugin(CIPluginInterface):
    def detect_language(self, project_path: str) -> Optional[str]:
        """
        Detects if the project is a Node.js project.
        """
        if os.path.exists(os.path.join(project_path, "package.json")):
            return "nodejs"
        return None

    def get_dependencies(self, project_path: str) -> dict[str, str]:
        """
        Detects the testing framework and linter used in the project.
        """
        dependencies = {"test": None, "linter": None}
        package_json_path = os.path.join(project_path, "package.json")
        if os.path.exists(package_json_path):
            with open(package_json_path, "r", encoding="utf-8") as f:
                try:
                    package_json = json.load(f)
                    dev_dependencies = package_json.get("devDependencies", {})
                    dependencies["test"] = (
                        "jest" if "jest" in dev_dependencies else "mocha" if "mocha" in dev_dependencies else None
                    )
                    dependencies["linter"] = "eslint" if "eslint" in dev_dependencies else None
                except json.JSONDecodeError:
                    print(i18n.get_message("errors", "package_json_decode"))
        return dependencies

    def generate_workflow(self, language: str, test: str, linter: str) -> str:
        """
        Generates the content of the .github/workflows/main.yml file for Node.js.
        """
        context = {
            "language": language,
            "version": "3.9",
            "test": test,
            "linter": linter,
        }

        return template.render("ci_template.yml.j2", context)
