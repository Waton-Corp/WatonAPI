from setuptools import setup, find_packages

setup(
    name="WatonAPI",
    version="0.1",
    author="DevBPM, lamorisi0n",
    url="https://github.com/Waton-Corp/WatonAPI",
    license="GPL-3.0",
    description="Python API for the WatonPlugin",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=[
        "dnspython==2.1.0",
    ],
    classifiers=[
        "Operating System :: OS Independent",
    ]
)
