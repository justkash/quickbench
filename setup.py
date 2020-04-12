from setuptools import setup, find_packages
from pathlib import Path
import quickbench

README_PATH = "./README.md"

long_description = Path(README_PATH).read_text()

setup(
    name=quickbench.__name__,
    version=quickbench.__version__,
    author=quickbench.__author__,
    author_email=None,
    url="https://github.com/justkash/quickbench",
    description="Utility to measure memory usage and execution time for a given program process.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="MIT",
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "quickbench = quickbench.quickbench:run_quickbench"
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    keywords="python3 quickbench benchmark measure utility commandline",
    python_requires=">=3.4",
    install_requires=None,
    zip_safe=True
)
