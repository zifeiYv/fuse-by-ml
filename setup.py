# -*- coding: utf-8 -*-
# 用于Cyhton的编译与发布
from setuptools import setup
from Cython.Build import cythonize

setup(
    ext_modules=cythonize([
        "fuse_utils.py",
        "fuse_yn.py",
        "utils.py"
    ],
        annotate=True)
)
