from setuptools import setup, find_packages

# For `pip install -e .`, editable install, pyproject.toml is not sufficient yet.
# Classic setup.py still required.
setup(name="specialsreplacer", packages=find_packages())
