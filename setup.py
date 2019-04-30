#!/usr/bin/env python

from setuptools import setup, find_packages


setup(
    name='bandits',
    version='0.0.1',
    description='Mult-armed Bandits introdutory package',
    author='Raphael Ottoni',
    author_email='rapha.ottoni@gmail.com',
    include_package_data=True,
    package_data={},
    packages=find_packages(),
    install_requires=[
        'numpy==1.16.3',
    ]
)
