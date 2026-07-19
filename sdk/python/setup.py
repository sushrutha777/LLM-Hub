from setuptools import setup, find_packages

setup(
    name="llmhub-sdk",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "httpx>=0.20.0",
    ],
    author="LLMHub",
    description="Python client SDK for the LLMHub AI Gateway",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)
