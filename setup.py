from setuptools import setup

with open('README.md', 'r') as f:
    README = f.read()

setup(
    name='devcmd',
    author='Devon (Gorialis) R',
    url='https://github.com/Cyber-Incorporated/devcmd',

    license='MIT',
    description='a developer tool for discord.py discord bots',
    long_description=README,
    project_urls={
        'Code': 'https://github.com/Cyber-Incorporated/devcmd',
        'Issue tracker': 'https://github.com/Cyber-Incorporated/devcmd/issues'
    },

    version='0.0.1',
    packages=['devcmd'],
    include_package_data=True,
    python_requires='>=3.8.0',

    download_url=f'https://github.com/Cyber-Incorporated/devcmd/blob/main/dist/devcmd-1.0.0.tar.gz',

    classifiers = [
    "Programming Language :: Python :: 3",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
    ]
)