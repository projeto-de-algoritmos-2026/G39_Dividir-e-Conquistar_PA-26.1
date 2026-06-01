from setuptools import setup, find_packages

setup(
    name="statrank",
    version="0.1.0",
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "statrank=statrank.cli:main",
        ]
    },
    install_requires=["matplotlib"],
    python_requires=">=3.8",
)
