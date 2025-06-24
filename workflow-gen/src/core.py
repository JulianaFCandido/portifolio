import os
from typing import Optional, Dict

import click

from src.plugins import CIPluginInterface, PluginLoader
from src.exceptions import LanguageDetectionError
from src.utils import i18n


def detect_language_from_project(project_path: str, plugins: Dict[str, CIPluginInterface]) -> Optional[str]:
    """
    Detects the language from an existing project.
    """
    for plugin_name, plugin in plugins.items():
        try:
            instance = plugin()
            language = instance.detect_language(project_path)
            if language:
                return language
        except Exception as e:
            print(i18n.get_message("errors", "plugin_error", plugin_name=plugin_name, error=e))
            return None
    return None


@click.command()
@click.option(
    "--project",
    "-p",
    type=click.Path(exists=True, file_okay=False, dir_okay=True),
    help=i18n.get_message("help", "project"),
)
@click.option(
    "--language",
    "-l",
    type=click.Choice(["nodejs", "python", "java"]),
    help=i18n.get_message("help", "language"),
)
@click.option(
    "--frontend",
    "-f",
    type=click.Choice(["react", "angular", "vue"]),
    help=i18n.get_message("help", "frontend"),
)
@click.option(
    "--test",
    "-t",
    type=click.Choice(["jest", "mocha", "pytest", "unittest", "junit", "karma", "jasmine"]),
    help=i18n.get_message("help", "test"),
)
@click.option(
    "--linter",
    "-i",
    type=click.Choice(["eslint", "flake8", "pylint", "checkstyle"]),
    help=i18n.get_message("help", "linter"),
)
@click.option(
    "--output",
    "-o",
    type=click.Path(file_okay=False, dir_okay=True),
    help=i18n.get_message("help", "output"),
)
def cli(project: str, language: str, frontend: str, test: str, linter: str, output: str):
    """
    WorkflowGen for GitHub Actions
    """
    plugin_loader = PluginLoader()
    plugins = plugin_loader.load_plugins()

    try:
        if project:
            language = detect_language_from_project(project, plugins)
            if not language:
                raise LanguageDetectionError(i18n.get_message("errors", "language_detection_error"))

        if not language:
            raise click.UsageError(i18n.get_message("errors", "usage_error"))

        plugin = plugins.get(language)
        if not plugin:
            raise click.ClickException(i18n.get_message("errors", "language_not_supported", language=language))

        instance = plugin()

        if project:
            dependencies = instance.get_dependencies(project)
            test = dependencies.get("test")
            linter = dependencies.get("linter")

        workflow_content = instance.generate_workflow(language, test, linter)
        output_dir = output or os.path.join(project or ".", ".github", "workflows")

        os.makedirs(output_dir, exist_ok=True)
        output_file = os.path.join(output_dir, "main.yml")

        with open(output_file, "w") as f:
            f.write(workflow_content)

        click.echo(i18n.get_message("messages", "workflow_generated", output_file=output_file))

    except LanguageDetectionError as e:
        click.echo(str(e), err=True)
    except click.UsageError as e:
        click.echo(str(e), err=True)
    except click.ClickException as e:
        click.echo(str(e), err=True)
