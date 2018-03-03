#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Copyright 2018 Fedele Mantuano (https://www.linkedin.com/in/fmantuano/)

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

import os
import runpy
from setuptools import setup


current = os.path.realpath(os.path.dirname(__file__))

with open(os.path.join(current, 'README.rst')) as f:
    long_description = f.read().strip()

with open(os.path.join(current, 'requirements.txt')) as f:
    requires = f.read().splitlines()

__version__ = runpy.run_path(
    os.path.join(current, "fetcher", "version.py"))["__version__"]


setup(
    name='untroubled-spam-fetcher',
    description="This tool gets the Untroubled spam mails",
    license="Apache License, Version 2.0",
    url="https://github.com/SpamScope/untroubled-spam-fetcher",
    long_description=long_description,
    version=__version__,
    author="Fedele Mantuano",
    author_email="mantuano.fedele@gmail.com",
    maintainer="Fedele Mantuano",
    maintainer_email='mantuano.fedele@gmail.com',
    packages=["fetcher"],
    platforms=["Linux"],
    keywords=['mail', 'email', 'fetcher', 'untroubled'],
    classifiers=[
        "License :: OSI Approved :: Apache Software License",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
    ],
    install_requires=requires,
    entry_points={'console_scripts': [
        'untroubled-spam-fetcher = fetcher.fetcher:main']},
)
