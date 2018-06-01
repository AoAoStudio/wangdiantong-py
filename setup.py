# -*- coding: utf-8 -*-
import sys
from os.path import dirname, abspath, join

from pip.req import parse_requirements
from setuptools import setup, find_packages

LIB_DIR = dirname(abspath(__file__))


def long_description():
    with open(join(LIB_DIR, 'README.md')) as readme_file:
        readme = readme_file.read()

    with open(join(LIB_DIR, 'HISTORY.md')) as history_file:
        history = history_file.read()
    return readme + '\n\n' + history


requirements = [str(ir.req)
                for ir in
                parse_requirements(join(LIB_DIR, 'requirements', 'base.txt'),
                                   session='hack')]

test_requirements = [str(ir.req)
                     for ir in parse_requirements(
        join(LIB_DIR, 'requirements', 'local.txt'), session='hack')]

sys.path.insert(0, LIB_DIR)
import wangdiantong as wdt

setup(
    name='wangdiantong-py',
    packages=find_packages(exclude=['tests']),
    version='0.0.3',
    description="wangdiantong python openapi",
    long_description=long_description(),
    author=wdt.__author__,
    author_email=wdt.__email__,
    url='https://github.com/ranger-huang/wangdiantong-py/git',
    entry_points={
        'console_scripts': [
        ]
    },
    include_package_data=True,
    install_requires=requirements,
    zip_safe=False,
    keywords='wangdiantong',
    classifiers=[
        'Development Status :: 1 - Pre-Alpha',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    test_suite='nose.collector',
    tests_require=test_requirements
)
