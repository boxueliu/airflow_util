# -*- coding:UTF-8 -*-
#!/usr/bin/env python
from __future__ import print_function
from setuptools import setup, find_packages
import sys

setup(
    name="airflowUtil",
    version="0.2.0",
    author="boxue liu",
    author_email="liu.boxue@detvista.com",
    license="Apache License",
    url="https://github.com/boxueliu/airflow_util",
    packages=["AirflowUtil"],
    install_requires=["cx_Oracle", "traceback2"],
    classifiers=[
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Topic :: Text Processing :: Indexing",
        "Topic :: Utilities",
        "Topic :: Internet",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.6"
    ],
)
