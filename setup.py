from setuptools import setup

from devcmd import VERSION

with open("README.md", "r") as f:
    README = f.read()

with open("requirements.txt", "r") as f:
    requirements = f.read()

setup(
    name="devcmd",
    author="cibere",
    url="https://github.com/cibere/devcmd",
    license="MIT",
    description="a developer tool for discord.py discord bots",
    long_description=README,
    project_urls={
        "Code": "https://github.com/cibere/devcmd",
        "Issue tracker": "https://github.com/cibere/devcmd/issues",
    },
    version=VERSION,
    packages=["devcmd", "devcmd.sections"],
    include_package_data=True,
    install_requires=requirements,
    python_requires=">=3.8.0",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "License :: MIT License",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Internet",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Utilities",
    ],
)
