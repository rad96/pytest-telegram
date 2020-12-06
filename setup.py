#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = ['requests']

setup_requirements = ['pytest-runner', ]

test_requirements = ['pytest', ]

setup(
    author="Artem Ryabkov",
    author_email='rad964@gmail.com',
    classifiers=[
        'Framework :: Pytest',
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9'
    ],
    description="Pytest to Telegram reporting plugin",
    install_requires=requirements,
    license="MIT license",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords=[
        'pytest', 'py.test', 'telegram',
    ],
    name='pytest-telegram',
    packages=find_packages(include=['pytest_telegram']),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/rad96/pytest-telegram',
    version='1.0.2',
    zip_safe=False,
    entry_points={
        'pytest11': [
            'pytest-telegram = pytest_telegram.plugin',
        ]
    }
)
