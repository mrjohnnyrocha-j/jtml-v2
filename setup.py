# setup.py
import sys
import os
import setuptools
from setuptools import setup, Extension
from setuptools.command.build_ext import build_ext
import pybind11

extensions = [
    Extension(
        "jtml_engine",   # The resulting import name
        sources=[
            "jtml_elements/jtml_bindings.cpp",
            "jtml_elements/jtml_ast.cpp",
            "jtml_elements/jtml_interpreter.cpp",
            "jtml_elements/jtml_lexer.cpp",
            "jtml_elements/jtml_parser.cpp",
            "jtml_elements/jtml_transpiler.cpp"
        ],
        include_dirs=[
            "jtml_elements",   # for your headers
            pybind11.get_include(),
            pybind11.get_include(user=True),
        ],
        language="c++",
        extra_compile_args=["-std=c++17", "-O3", "-Wall"],
    )
]

setup(
    name="opalg",
    version="0.1.0",
    # This finds your Python packages
    packages=setuptools.find_packages(),
    # or something like packages=["opalg"], or package_dir=...

    ext_modules=extensions,
    cmdclass={"build_ext": build_ext},
)
