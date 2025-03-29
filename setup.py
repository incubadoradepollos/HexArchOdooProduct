from setuptools import setup, find_packages

setup(
    name="hexarch_product_odoo",
    version="0.1",
    packages=find_packages(),
    author="Jose Manuel Herrera Saenz",
    author_email="incubadoradepollos@gmail.com",
    description="Adaptador para productos contra ecomerce de ODOO",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/incubadoradepollos/HexArchOdooProduct.git",
    install_requires=[
        "hexarch_core @ git+https://github.com/incubadoradepollos/HexArchCoreProduct.git"
    ],
   classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.12.4",
)