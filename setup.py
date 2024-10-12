# Path: setup.py
# Description: This script will contain the code to build the package.

import toml
from setuptools import find_packages, setup

# Load data from the poetry.toml file
def read_poetry_file(fname="pyproject.toml"):
    with open(fname, "r") as f:
        data = toml.load(f)
    return data

def get_dependencies(data):
    dependencies = data["tool"]["poetry"]["dependencies"]
    # Remove python version from dependencies
    dependencies.pop("python", None)
    return [f"{pkg}=={ver.replace('^', '')}" for pkg, ver in dependencies.items()]

def get_dev_dependencies(data):
    dev_dependencies = data["tool"]["poetry"]["group"]["dev"]["dependencies"]
    return [f"{pkg}=={ver.replace('^', '')}" for pkg, ver in dev_dependencies.items()]

# Read the poetry file
poetry_data = read_poetry_file()

# Set up the package
setup(
    name=poetry_data["tool"]["poetry"]["name"],
    py_modules=["ssi"],
    version=poetry_data["tool"]["poetry"]["version"],
    description=poetry_data["tool"]["poetry"]["description"],
    author=", ".join(poetry_data["tool"]["poetry"]["authors"]),
    license=poetry_data["tool"]["poetry"]["license"],
    packages=find_packages(),
    install_requires=get_dependencies(poetry_data),
    extras_require={
        "dev": get_dev_dependencies(poetry_data),
    },
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.9",
)
