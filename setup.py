#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages

with open('README.md') as readme_file:
    readme = readme_file.read()

requirements = [
    'Click',
    'numpy',
    'matplotlib',
    'pandas',
    'scipy',
    'seaborn',
    'python-dotenv',
    'Sphinx',
]

setup(
    author="userusr",
    author_email='userusr@yandex.ru',
    description="Template",
    install_requires=requirements,
    extras_require={
        'dev': [
            'pyment',
            'pip-tools',
        ]
    },
    license="MIT license",
    long_description=readme,
    include_package_data=True,
    name='template-da',
    packages=find_packages(),
    version='0.1.0',
)
