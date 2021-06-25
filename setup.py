"""
setup.py
"""
import os
import logging
from codecs import open
from pathlib import Path
from setuptools import setup, find_packages
from setuptools.command.develop import develop
from setuptools.command.install import install
from subprocess import check_call
import shlex
import sys

try:
    from jade.utils.subprocess_manager import run_command
except ImportError:
    print("jade must be installed prior to installing disco")
    sys.exit(1)

logger = logging.getLogger(__name__)


def read_lines(filename):
    return Path(filename).read_text().splitlines()



class PostDevelopCommand(develop):
    """Post-installation for development mode."""
    def run(self):
        develop.run(self)
        install_jade_extensions()


class PostInstallCommand(install):
    """Post-installation for installation mode."""
    def run(self):
        install.run(self)
        install_jade_extensions()


def install_jade_extensions():
    ext = os.path.join(here, "disco", "extensions", "jade_extensions.json")
    run_command(f"jade extensions register {ext}")
    run_command("jade extensions add-logger disco")


here = os.path.abspath(os.path.dirname(__file__))

with open("README.md", encoding="utf-8") as f:
    readme = f.read()

with open(os.path.join(here, "disco", "version.py"), encoding="utf-8") as f:
    version = f.read()

version = version.split()[2].strip('"').strip("'")

test_requires = ["pytest", ]

setup(
    name="disco",
    version=version,
    description="DISCO",
    long_description=readme,
    long_description_content_type="text/markdown",
    maintainer_email="daniel.thom@nrel.gov",
    url="https://github.com/NREL/disco",
    packages=find_packages(),
    package_dir={"disco": "disco"},
    entry_points={
        "console_scripts": [
            "disco=disco.cli.disco:cli",
            "disco-internal=disco.cli.disco_internal:cli",
        ],
    },
    include_package_data=True,
    license="BSD license",
    zip_safe=False,
    keywords=["disco"],
    python_requires=">=3.7",
    classifiers=[
        "Development Status :: Alpha",
        "Intended Audience :: Modelers",
        "License :: OSI Approved :: BSD License",
        "Natural Language :: English",
        "Programming Language :: Python :: 3.7",
    ],
    test_suite="tests",
    install_requires=read_lines("requirements.txt"),
    extras_require={
        "dev": read_lines("dev-requirements.txt"),
    },
    cmdclass={"install": PostInstallCommand, "develop": PostDevelopCommand},
)
