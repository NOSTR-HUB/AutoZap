from setuptools import setup, find_packages

setup(
    name="autozap",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "python-nostr>=0.5.0",
        "python-dotenv>=1.0.0",
        "requests>=2.31.0",
    ],
    python_requires=">=3.10",
)