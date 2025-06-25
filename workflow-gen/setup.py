"""
Package setup for workflow-gen.

This file configures how the package is built, its dependencies,
and how it is installed.  It uses setuptools to define the package
metadata and entry points.
"""

from setuptools import setup, find_packages

setup(
    name="workflow-gen",
    version="0.1.0",
    packages=find_packages(include=["src", "src.*"]),
    install_requires=[
        "click",
        "pyyaml",
        "jinja2",
    ],
    extras_require={
        "dev": [
            "black",
            "flake8",
            "pylint",
        ],
    },
    entry_points={
        "console_scripts": [
            "workflow-gen=src.core:cli",
        ],
    },
)
