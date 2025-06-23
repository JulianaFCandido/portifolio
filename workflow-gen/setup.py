from setuptools import setup, find_packages

setup(
    name='workflow-gen',
    version='0.1.0',
    packages=find_packages(include=['src', 'src.*']),
    install_requires=[
        'Click',
        'PyYAML',
    ],
    entry_points={
        'console_scripts': [
            'workflow-gen=src.core:cli',
        ],
    },
)
