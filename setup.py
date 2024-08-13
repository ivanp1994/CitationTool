# -*- coding: utf-8 -*-
"""
Created on Tue Aug 13 08:14:47 2024

@author: ivanp
"""


from setuptools import setup

with open("README.md", "r") as _f:
    long_description = _f.read()

with open("requirements.txt", "r") as _f:
    install_reqs = _f.read().strip().split("\n")

setup(name="CitaTool",
      version="0.0.1",
      description="DOI finder",
      package_dir={"src": "src"},
      long_description=long_description,
      long_description_content_type='text/markdown',
      url="https://github.com/ivanp1994/CitationTool/tree/main",
      author="Ivan Pokrovac",
      author_email="ivan.pokrovac.fbf@gmail.com",
      license="MIT",
      classifiers=["Development Status :: 3 - Alpha",
                   "License :: OSI Approved :: MIT License",
                   "Programming Language :: Python :: 3.8",
                   "Programming Language :: Python :: 3 :: Only",
                   "Intended Audience :: Science/Research"],
      install_requires=install_reqs,
      python_requires=">=3.8",
      entry_points={
          'console_scripts': [
              'citatool = src.gui:run_application',
          ]}
      )
