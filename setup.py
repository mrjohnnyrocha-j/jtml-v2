# setup.py

from setuptools import setup, find_packages, Extension
import pybind11
from setuptools.command.build_ext import build_ext
import sys
import os

class get_pybind_include(object):
    """Helper class to determine the pybind11 include path
    The purpose of this class is to postpone importing pybind11
    until it is actually installed, so that the `get_include()`
    method can be invoked. """

    def __init__(self, user=False):
        self.user = user

    def __str__(self):
        return pybind11.get_include(self.user)

ext_modules = [
    Extension(
        'jtmlparser',  # Name of the Python module
        ['jtml_parser_bindings.cpp'],  # Source file
        include_dirs=[
            get_pybind_include(),
            get_pybind_include(user=True),
            '/opt/homebrew/Cellar/antlr4-cpp-runtime/4.13.2/include/antlr4-runtime',  # ANTLR4 runtime include
        ],
        library_dirs=[
            '/opt/homebrew/Cellar/antlr4-cpp-runtime/4.13.2/lib',  # ANTLR4 runtime lib
        ],
        libraries=['antlr4-runtime'],  # Link against the ANTLR4 runtime library
        language='c++',
        extra_compile_args=['-std=c++17'],
    ),
]

setup(
    name='jtml_compiler',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'ply',
        'mkdocs',
        'mkdocs-material',
        'pybind11>=2.5.0',
    ],
    ext_modules=ext_modules,
    cmdclass={'build_ext': build_ext},
    entry_points={
        'console_scripts': [
            'jtml-compile=compiler.compiler:main',
            'jtml-interpreter=interpreter.interpreter:main',
        ],
    },
    author='Your Name',
    author_email='your.email@example.com',
    description='JTML Compiler and Interpreter',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/yourusername/jtml_compiler',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.7',
)
