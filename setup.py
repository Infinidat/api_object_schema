import os
from setuptools import setup, find_packages

with open(os.path.join(os.path.dirname(__file__), "api_object_schema", "__version__.py")) as version_file:
    exec(version_file.read())  # pylint: disable=exec-used

_INSTALL_REQUIERS = ["sentinels"]

setup(name="api_object_schema",
      classifiers=[
          "Programming Language :: Python :: 2.7",
          "Programming Language :: Python :: 3.5",
          "Programming Language :: Python :: 3.6",
          ],
      description="Utilities for defining schemas of Pythonic objects interacting with external APIs",
      license="BSD3",
      author="Infinidat Ltd.",
      author_email="info@infinidat.com",
      version=__version__,  # pylint: disable=undefined-variable
      packages=find_packages(exclude=["tests"]),

      url="https://github.com/Infinidat/api_object_schema",

      install_requires=_INSTALL_REQUIERS,
      scripts=[],
      namespace_packages=[]
     )
