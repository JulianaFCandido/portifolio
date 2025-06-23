import os
from core import CIPluginInterface
from typing import Optional

class JavaPlugin(CIPluginInterface):
    def detect_language(self, project_path: str) -> Optional[str]:
        """
        Detects if the project is a Java project.
        """
        if os.path.exists(os.path.join(project_path, "pom.xml")) or \
           os.path.exists(os.path.join(project_path, "build.gradle")):
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
      - name: Set up JDK 17
        uses: actions/setup-java@v3
        with:
          java-version: '17'
          distribution: 'temurin'
      - name: Validate Gradle wrapper
        uses: gradle/wrapper-validation-action@v1
      - name: Build with Gradle
        uses: gradle/gradle-build-action@v2
        with:
          arguments: build
"""
        return workflow_content
