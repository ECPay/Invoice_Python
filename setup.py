#!/usr/bin/env python
# -*- encoding: UTF-8 -*-
from setuptools import setup, find_packages
import io

VERSION = '1.1.1'

with io.open("README.rst", encoding='utf-8') as f:
    long_description = f.read()

install_requires = open("requirements.txt").readlines()

setup(
    name="ecpay_invoice3",
    version=VERSION,
    author="Hiskyz",
    author_email="skypc785308@gmail.com",
    url="https://github.com/skypc785308/ecpay_invoice3",
    description="ecpay_invoice3",
    long_description=long_description,
    packages=find_packages(),
    include_package_data=True,
    license='Apache 2.0 License',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Operating System :: OS Independent',
        'Intended Audience :: Financial and Insurance Industry',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6',
        'Topic :: Software Development :: Libraries'
    ],
    install_requires=install_requires,
)
