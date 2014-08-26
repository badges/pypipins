import os
import sys
from setuptools import setup, find_packages

setup(
    name='pypipins',
    version='0.0.0',
    description='Badges for your site to display download totals, latest version using crate.io https://pypip.in',
    # long_description=long_description,
    author='Kura',
    author_email='kura@kura.io',
    url='https://github.com/badges/pypipins',
    packages=find_packages(),
    zip_safe=True,
    keywords='PyPI crate.io badges pins',
    install_requires=[
        'Twisted>=13.2.0',
        'klein>=0.2.3',
        'requests>=2.2.1',
        'yarg>=0.1.9',
        'redis>=2.10.3'
    ],
    classifiers=[
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Natural Language :: English',
        'Intended Audience :: Developers',
    ],
)
