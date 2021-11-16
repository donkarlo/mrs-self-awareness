#! /usr/bin/env python3
# -*- coding: utf-8 -*-


from distutils.core import setup
from catkin_pkg.python_setup import generate_distutils_setup

d = generate_distutils_setup(
    packages=['uavRoles'],
    package_dir={'': 'scripts'}
)

setup(**d)
