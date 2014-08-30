import os
import sys
from setuptools import setup, find_packages

setup(
    name='pypipins',
    version='0.0.0',
    description='Badges for your site to display download totals, latest version using PyPI https://pypip.in',
    # long_description=long_description,
    author='Kura',
    author_email='kura@kura.io',
    url='https://github.com/badges/pypipins',
    packages=find_packages(),
    zip_safe=True,
    keywords='PyPI badges/pins/shields',
    install_requires=[
        'Twisted',
        'klein',
        'requests',
        'yarg',
        'redis'
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
