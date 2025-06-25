"""
Provides internationalization (i18n) support for the application.

Loads localized messages from a YAML file and provides a function to retrieve
messages based on category and key. Supports formatting messages with arguments.
"""

import os
import yaml

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
I18N_PATH = os.path.join(BASE_DIR, "../resources/i18n.yml")

with open(I18N_PATH, "r", encoding="utf-8") as f:
    _messages = yaml.safe_load(f)


def get_message(category, key, **kwargs):
    """
    Retrieve the localized message based on the category and key.
    Supports formatting with arguments via str.format().
    """
    try:
        message = _messages[category][key]
        if kwargs:
            message = message.format(**kwargs)
        return message
    except KeyError:
        return f"Message not found for {category}.{key}"
