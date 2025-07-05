from setuptools import setup, find_packages

setup(
    name='myproject',  # Replace 'myproject' with the name of your project
    version='0.1.0',
    packages=find_packages(where="server") + \
        #find_packages(where="web_client") + \
        find_packages(where="lib"),
    package_dir={'': 'src'},  # Specifies that packages are located in the 'src' directory
    python_requires='>=3.12', # Specify the Python versions you support
)
