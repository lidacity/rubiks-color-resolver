from setuptools import setup


setup(
    name="rubiks_color_resolver",
    version="1.0.0",
    description="Resolve rubiks cube RGB values to the six cube colors",
    keywords="rubiks cube color",
    url="https://github.com/lidacity/rubiks-color-resolver",
    author="lidacity",
    author_email="dzmitry@lidacity.by",
    license="GPLv3",
    scripts=["usr/bin/rubiks-color-resolver.py"],
    packages=["rubiks_color_resolver"],
)
