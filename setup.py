from setuptools import setup, find_packages

setup(
    name="govee_lan_control",
    version="1.0.2",
    packages=find_packages(),
    include_package_data=True,
    description="A Python package to control Govee LED devices over the local network using multicast UDP packets.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/my_package",
    author="Sharath Srinivasan",
    author_email="srinivasansharath@gmail.com",
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)