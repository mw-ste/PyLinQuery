# -*- coding: utf-8 -*-
"""
Created on Tue Dec 24 11:24:34 2019

@author: michi
"""

import setuptools

with open("README.md", "r") as fid:
    long_description = fid.read()

setuptools.setup(
    name="pylinquery",
    version="0.1.0",
    author="Michael Stenger",
    author_email="michael.stenger@outlook.de",
    description="Simple adaption of the C# LinQ syntax for Python 3",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/mw-ste/PyLinQuery",
    packages=["pylinquery"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.5',
)