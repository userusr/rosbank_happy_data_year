#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages

with open('README.md') as readme_file:
    readme = readme_file.read()

requirements = [
    'Click',
    'numpy',
    'pandas',
    'scipy',
    'seaborn',
    'python-dotenv',
    'Sphinx',
    'overpy',
    'geopandas',
    'jupyter',
    'jupyter_contrib_nbextensions',
    'jupyter_nbextensions_configurator',
    'autopep8',
    'matplotlib',
    'sklearn',
    'lightgbm',
    'ipyleaflet',
    'tqdm',
    'feather-format',
    'pyarrow',
    'isort',
    'selenium'
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
    name='rosbank_happy_data_year',
    packages=find_packages(),
    version='0.1.0',
)
