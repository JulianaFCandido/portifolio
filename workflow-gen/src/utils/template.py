"""
Provides template rendering functionality using Jinja2.

Loads Jinja2 templates from a specified directory and provides a function to
render templates with a given context.
"""

import os
from jinja2 import Environment, FileSystemLoader

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATES_PATH = os.path.join(BASE_DIR, "../templates")


def render(template_name: str, context: dict) -> str:
    """
    Renders a Jinja2 template.
    """
    env = Environment(loader=FileSystemLoader(TEMPLATES_PATH))
    template = env.get_template(template_name)
    return template.render(context)
