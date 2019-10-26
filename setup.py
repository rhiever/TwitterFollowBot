#!/usr/bin/env python
# -*- coding: utf-8 -*-
from setuptools import setup, find_packages
import os
import subprocess
from setuptools.command import easy_install


def parse_requirements(filename):
    return list(filter(lambda line: (line.strip())[0] != '#',
                       [line.strip() for line in open(filename).readlines()]))


def calculate_version():
    # Fetch version from git tags, and write to version.py.
    # Also, when git is not available (PyPi package), use stored version.py.
    version_py = os.path.join(os.path.dirname(__file__), 'version.py')
    try:
        version_git = subprocess.check_output(["git", "tag"]).rstrip().split("\n")[-1]
    except Exception:
        with open(version_py, 'r') as fh:
            version_git = (open(version_py).read()
                           .strip().split('=')[-1].replace('"', ''))
    version_msg = ('# OK')
    with open(version_py, 'w') as fh:
        fh.write(version_msg + os.linesep + "__version__=" + version_git)
    return version_git


requirements = parse_requirements('requirements.txt')
version_git = calculate_version()


def get_long_description():
    readme_file = 'README.md'
    if not os.path.isfile(readme_file):
        return ''
    # Try to transform the README from Markdown to reStructuredText.
    try:
        easy_install.main(['-U', 'pyandoc==0.0.1'])
        import pandoc
        pandoc.core.PANDOC_PATH = 'pandoc'
        doc = pandoc.Document()
        doc.markdown = open(readme_file).read()
        description = doc.rst
    except Exception:
        description = open(readme_file).read()
    return description


setup(
    name='TwitterBot',
    version=version_git,
    author='Unkown',
    author_email='blablabla@gmail.com',
    packages=find_packages(),
    url='https://github.com/JumperHacktivist/TwitterFollowBot',
    license='GNU/GPLv3',
    description=('A Python bot that automates several actions on Twitter, '
                 'such as following users and favoriting tweets.'),
    long_description=get_long_description(),
    zip_safe=True,
    install_requires=requirements,
    classifiers=[
        "Intended Audience :: Science/Research",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.2",
        "Programming Language :: Python :: 3.3",
        "Topic :: Boobs"
    ],
    keywords=['Twitter', 'followers', 'automation', 'bot'],
)
