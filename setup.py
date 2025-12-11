from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="rtg_api",
    version="1.0.0",
    author="Ghosteined",
    author_email="ghosteined@gmail.com",
    description="A Python library to create roblox Road to Gramby's creation codes from code",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Ghosteined/rtg_api",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.7",
    install_requires=[
        "typing_extensions",
        "rbxm_parser @ git+https://github.com/Ghosteined/rtg_api.git"
    ],
    keywords="roblox road to gramby's rtg python",
    project_urls={
        "Bug Reports": "https://github.com/Ghosteined/rtg_api/issues",
        "Source": "https://github.com/Ghosteined/rtg_api",
    },
)