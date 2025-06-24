from setuptools import setup, find_packages

setup(
    name="workflow-gen",
    version="0.1.0",
    packages=find_packages(include=["src", "src.*"]),
    install_requires=[
        "black",
        "click",
        "flake8",
        "jinja2",
        "pylint",
        "pyyaml",
    ],
    setup_requires=[
        "setuptools",
    ],
    entry_points={
        "console_scripts": [
            "workflow-gen=src.core:cli",
        ],
    },
)
