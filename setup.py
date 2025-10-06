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

# Read the contents of README.md
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding='utf-8')

# Read version from package
def get_version():
    version_file = this_directory / "githydra" / "__init__.py"
    with open(version_file, 'r', encoding='utf-8') as f:
        for line in f:
            if line.startswith('__version__'):
                return line.split('=')[1].strip().strip('"\'')
    return "3.1.0"

setup(
    name='githydra',
    version=get_version(),
    description='Comprehensive Git Automation CLI Tool with Beautiful Terminal UI and Template Management',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Abdulaziz Alqudimi',
    author_email='eng7mi@gmail.com',
    url='https://github.com/Alqudimi/GitHydra',
    project_urls={
        'Bug Reports': 'https://github.com/Alqudimi/GitHydra/issues',
        'Source': 'https://github.com/Alqudimi/GitHydra',
        'Documentation': 'https://github.com/Alqudimi/GitHydra/tree/main/docs',
        'Changelog': 'https://github.com/Alqudimi/GitHydra/releases',
    },
    packages=find_packages(),
    include_package_data=True,
    python_requires='>=3.8',
    install_requires=[
        'click>=8.1.0',
        'colorama>=0.4.6',
        'gitpython>=3.1.40',
        'pyyaml>=6.0',
        'questionary>=2.0.0',
        'rich>=13.7.0',
        'pygithub>=2.8.0',
        'tqdm>=4.65.0',
    ],
    entry_points={
        'console_scripts': [
            'githydra=githydra.__main__:cli',
        ],
    },
    classifiers=[
        # Development Status
        'Development Status :: 5 - Production/Stable',
        
        # Intended Audience
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Intended Audience :: Information Technology',
        
        # Topics
        'Topic :: Software Development :: Version Control :: Git',
        'Topic :: Software Development :: User Interfaces',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: System :: Shells',
        'Topic :: Terminals',
        'Topic :: Utilities',
        
        # License
        'License :: OSI Approved :: MIT License',
        
        # Programming Languages
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        
        # Operating Systems
        'Operating System :: OS Independent',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX',
        'Operating System :: Unix',
        'Operating System :: MacOS',
        
        # Environment
        'Environment :: Console',
        'Environment :: Console :: Curses',
        
        # Natural Languages
        'Natural Language :: English',
        'Natural Language :: Arabic',
        
        # Frameworks (استخدم التصنيفات الصحيحة فقط)
        'Framework :: AsyncIO',
        'Framework :: Buildout',
    ],
    keywords=[
        'git',
        'cli',
        'automation',
        'terminal',
        'ui',
        'version-control',
        'developer-tools',
        'productivity',
        'templates',
        'project-management',
        'collaboration',
        'command-line',
        'rich',
        'github',
        'gitlab',
    ],
    license='MIT',
    zip_safe=False,
    platforms=['any'],
)