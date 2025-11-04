from setuptools import setup, find_packages

setup(
    name="poradock-logging",
    version="1.0.0",
    description="Python клиент для API логирования Poradock",
    author="Aleksey Mayka",
    packages=find_packages(),
    install_requires=[
        "requests>=2.31.0",
    ],
    python_requires=">=3.7",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
)

