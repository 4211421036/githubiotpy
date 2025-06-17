from setuptools import setup, find_packages
import os

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="githubiot",
    version="1.0.5",
    author= "GALIH RIDHO UTOMO, Fionita Fahra Azzahra",
    author_email= "g4lihru@students.unnes.ac.id, fionitafahra13@students.unnes.ac.id",
    description="GitHubIoT is a comprehensive toolkit designed to simplify the visualization of IoT (Internet of Things) data with seamless GitHub integration. The application provides an intuitive graphical interface for real-time data monitoring, analysis, and configuration, making it ideal for both beginners and experienced developers working with IoT devices microcontroler (ESP32 or ESP8266) realtime",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/4211421036/githubiotpy",
    keyword="Github, IoT, Arduino IDE, Python Modules, ESP32, ESP8266, webApp",
    packages=find_packages(),
    include_package_data=True,
    package_data={
        "githubiot": ["templates/*"],
    },
    install_requires=[
        "requests>=2.26.0",
        "matplotlib>=3.5.0", 
        "numpy>=1.21.0",
        "pyinstaller>=5.0.0",
    ],
    entry_points={
        "console_scripts": [
            "githubiot=githubiot.cli:run_cli",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
