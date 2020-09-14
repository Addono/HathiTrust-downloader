#!/usr/bin/env python
#  -*- coding: utf-8 -*-


from setuptools import setup, find_packages
import os

import hathitrustdownloader


setup(
    name='hathitrust-downloader',
    version=os.environ.get('HATHITRUST_DOWNLOADER_VERSION', '0.0.0'),
    description='Downloads multiple pages from Hathitrust from the CLI.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='http://github.com/addono/hathitrust-downloader',
    author='Adriaan Knapen',
    author_email='hi@aknapen.nl',
    license='MIT',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Operating System :: POSIX',
        'Operating System :: POSIX :: Linux',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    keywords='hathitrust download downloader cli',
    packages=find_packages(),
    install_requires=[
        'requests==2.24.0',
        'tqdm==4.48.2',
    ],
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'hathitrust-downloader=hathitrustdownloader.cli:main',
        ],
    }
)

