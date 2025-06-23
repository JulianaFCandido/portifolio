import click
import os
import importlib
from typing import Optional, Dict, Any
import yaml
import inspect

class CIPluginInterface:
    def detect_language(self, project_path: str) -> Optional[str]:
        """
        Detects the programming language of the project.
        """
        raise NotImplementedError

    def get_dependencies(self, project_path: str) -> dict[str, str]:
        """
        Detects the testing framework and linter used in the project.
        """
        raise NotImplementedError

    def generate_workflow(self, language: str, test: str, linter: str) -> str:
        """
        Generates the content of the .github/workflows/main.yml file.
        """
        raise NotImplementedError


def load_plugins(plugin_dir="plugins") -> dict[str, CIPluginInterface]:
    """
    Loads plugins from the specified directory.
    """
    plugins: dict[str, CIPluginInterface] = {}
    for filename in os.listdir(plugin_dir):
        if filename.endswith(".py") and filename != "__init__.py":
            module_name = filename[:-3]
            module_path = f"{plugin_dir}.{module_name}"
            try:
                module = importlib.import_module(module_path)
                for name, obj in inspect.getmembers(module):
                    if inspect.isclass(obj):
                        plugin_class = getattr(module, name)
                        plugins[module_name] = plugin_class
            except Exception as e:
                print(f"Error loading plugin {module_name}: {e}")
    return plugins

def detect_language_from_project(project_path: str, plugins: dict) -> Optional[str]:
    """
    Detects the language from existing project
    """
    for plugin_name, plugin in plugins.items():
        try:
            instance = plugin()
            language = instance.detect_language(project_path)
            if language:
                return language
        except Exception as e:
            print(f"Erro ao executar o plugin {plugin_name}: {e}")
            return None
    return None

@click.command()
@click.option('--project', '-p', type=click.Path(exists=True, file_okay=False, dir_okay=True),
              help='Path to the project directory (for existing projects).')
@click.option('--language', '-l', type=click.Choice(['nodejs', 'python', 'java']),
              help='Programming language of the project (for new projects).')
@click.option('--frontend', '-f', type=click.Choice(['react', 'angular', 'vue']),
              help='Frontend framework of the project (for new projects).')
@click.option('--test', '-t', type=click.Choice(['jest', 'mocha', 'pytest', 'unittest', 'junit', 'karma', 'jasmine']),
              help='Testing framework of the project (for new projects).')
@click.option('--linter', '-i', type=click.Choice(['eslint', 'flake8', 'pylint', 'checkstyle']),
              help='Linter of the project (for new projects).')
@click.option('--output', '-o', type=click.Path(file_okay=False, dir_okay=True),
              help='Specify a different directory for storing the .github/workflows/main.yml.')
def cli(project: str, language: str, frontend: str, test: str, linter: str, output: str):
    """
    WorkflowGen for GitHub Actions
    """
    plugins = load_plugins()

    if project:
        language = detect_language_from_project(project, plugins)
        if not language:
            click.echo("Could not detect language from project. Please specify using --language.")
            return

    if not language:
        click.echo("Please specify the language using --language or provide the project path using --project.")
        return

    plugin = plugins.get(language)

    if not plugin:
        click.echo(f"Language {language} not supported.")
        return

    try:
        instance = plugin()

        if project:
            dependencies = instance.get_dependencies(project)
            test = dependencies.get("test")
            linter = dependencies.get("linter")

        workflow_content = instance.generate_workflow(language, test, linter)
        output_dir = output or os.path.join(project or ".", ".github", "workflows")
    except Exception as e:
        print(f"Erro ao executar o plugin: {e}")
        return

    os.makedirs(output_dir, exist_ok=True)
    output_file = os.path.join(output_dir, "main.yml")

    with open(output_file, "w") as f:
        f.write(workflow_content)

    click.echo(f"Generated workflow file: {output_file}")


if __name__ == '__main__':
    cli()
