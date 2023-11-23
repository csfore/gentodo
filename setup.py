from setuptools import setup
from gentodo.main import __version__ as version

setup(
    name="gentodo",
    version=version,
    description="A todo list app for Gentoo users, by a Gentoo user",
    author="csfore",
    entry_points={
        "console_scripts": [
            "gentodo = gentodo.main:main"
        ]
    }
)
