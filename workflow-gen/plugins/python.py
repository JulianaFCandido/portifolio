import os
from core import CIPluginInterface
from typing import Optional

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
            with open(os.path.join(project_path, "requirements.txt"), "r") as f:
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
        # Basic workflow content (you can customize this later)
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
      - name: Set up Python 3.9
        uses: actions/setup-python@v3
        with:
          python-version: "3.9"
      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install flake8 pytest
          if [ -f requirements.txt ]; then pip install -r requirements.txt; fi
      - name: Lint with flake8
        run: |
          flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
          flake8 . --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics
      - name: Test with pytest
        run: |
          pytest
"""
        return workflow_content
