#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
GitHydra - Comprehensive Git Automation CLI Tool
Author: Abdulaziz Alqudimi
Email: eng7mi@gmail.com
Repository: https://github.com/Alqudimi/GitHydra
"""

from setuptools import setup, find_packages
from pathlib import Path

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding='utf-8')

setup(
    name='githydra',
    version='3.0.0',
    description='Comprehensive Git Automation CLI Tool with Beautiful Terminal UI',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Abdulaziz Alqudimi',
    author_email='eng7mi@gmail.com',
    url='https://github.com/Alqudimi/GitHydra',
    project_urls={
        'Bug Reports': 'https://github.com/Alqudimi/GitHydra/issues',
        'Source': 'https://github.com/Alqudimi/GitHydra',
        'Documentation': 'https://github.com/Alqudimi/GitHydra/tree/main/docs',
    },
    packages=find_packages(),
    include_package_data=True,
    python_requires='>=3.11',
    install_requires=[
        'click>=8.1.0',
        'colorama>=0.4.6',
        'gitpython>=3.1.40',
        'pyyaml>=6.0',
        'questionary>=2.0.0',
        'rich>=13.7.0',
    ],
    entry_points={
        'console_scripts': [
            'githydra=githydra.__main__:main',
        ],
    },
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Version Control :: Git',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Operating System :: OS Independent',
        'Environment :: Console',
        'Natural Language :: English',
        'Natural Language :: Arabic',
    ],
    keywords='git cli automation terminal ui version-control developer-tools',
    license='MIT',
    zip_safe=False,
)
