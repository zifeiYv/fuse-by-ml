# -*- coding: utf-8 -*-
from setuptools import setup
from Cython.Build import cythonize

setup(
    ext_modules=cythonize(["fuse_utils.pyx",
                           "fuse_yn.pyx",
                           "utils.pyx"],
                          annotate=True)
)
