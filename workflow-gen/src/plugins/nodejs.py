import os
from src.plugins import CIPluginInterface
from typing import Optional
import json

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
            with open(package_json_path, "r") as f:
                try:
                    package_json = json.load(f)
                    dev_dependencies = package_json.get("devDependencies", {})
                    dependencies["test"] = "jest" if "jest" in dev_dependencies else "mocha" if "mocha" in dev_dependencies else None
                    dependencies["linter"] = "eslint" if "eslint" in dev_dependencies else None
                except json.JSONDecodeError:
                    print("Error decoding package.json")
        return dependencies

    def generate_workflow(self, language: str, test: str, linter: str) -> str:
        """
        Generates the content of the .github/workflows/main.yml file for Node.js.
        """
        workflow_content = f"""
name: CI

on:
  push:
    branches: [ "main" ]
  pull_request:
    branches: [ "main" ]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Set up Node.js
        uses: actions/setup-node@v3
        with:
          node-version: '16'
      - name: Install dependencies
        run: npm install
      - name: Run linters
        run: npm run lint
      - name: Run tests
        run: npm run test
"""
        return workflow_content
