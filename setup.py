import pathlib
from setuptools import setup, find_packages

HERE = pathlib.Path(__file__).parent

VERSION = "0.5.0"
PACKAGE_NAME = "crossposter"
AUTHOR = "Meet Gor"
AUTHOR_EMAIL = "gormeet711@gmail.com"
URL = "https://github.com/Mr-Destructive/crossposter"

DESCRIPTION = (
    "Crosspost your markdown articles to devto, medium, codenewbie and hashnode"
)
README = (pathlib.Path(__file__).parent / "README.md").read_text(encoding="utf-8")

INSTALL_REQUIRES = [
    "requests",
    "pyyaml",
    "python-frontmatter",
]

setup(
    name=PACKAGE_NAME,
    version=VERSION,
    description=DESCRIPTION,
    long_description=README,
    long_description_content_type="text/markdown",
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    url=URL,
    install_requires=INSTALL_REQUIRES,
    packages=find_packages(),
    entry_points={"console_scripts": ["crosspost = crossposter.app:main"]},
)
