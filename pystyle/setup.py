from setuptools import setup, find_packages

setup(
    name="pystyle-tk",
    version="1.0.0",
    author="Sythgirla",
    description="Dynamic tk/ttk color & style editor",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/Sythgirla/PyStyle",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Windows Only",
    ],
    python_requires=">=3.6",
    install_requires=["PyYAML>=6.0"],
    include_package_data=True
)