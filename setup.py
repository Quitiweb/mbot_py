from setuptools import setup, find_packages

setup(
    name="mbot-assistant",
    version="1.0.0",
    description="Voice Assistant for mBot robot with local AI",
    author="mBot Assistant Team",
    packages=find_packages(),
    install_requires=[
        "pyserial>=3.5",
        "bleak>=0.20.0",
        "pyaudio>=0.2.11",
        "speechrecognition>=3.10.0",
    ],
    python_requires=">=3.8",
    entry_points={
        "console_scripts": [
            "mbot-assistant=main:main",
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
)
