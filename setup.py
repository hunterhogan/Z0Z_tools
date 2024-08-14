from setuptools import setup, find_packages
from packaging.requirements import Requirement

with open('requirements.txt') as fileRequirements:
    listRequirements = [str(Requirement(requirement.strip())) for requirement in fileRequirements if requirement.strip()]

setup(
    name='Z0Z_tools',
    version='0.0.1',
    packages=find_packages(),
    install_requires=listRequirements,
    download_url='https://github.com/hunterhogan/Z0Z_tools.git',
)
# import re
# import os

# def get_version():
#     version_file = os.path.join(os.path.dirname(__file__), 'your_package', '__version__.py')
#     with open(version_file, 'r') as f:
#         version_line = f.read()
#     version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]", version_line, re.M)
#     if version_match:
#         return version_match.group(1)
#     raise RuntimeError("Unable to find version string.")

# from setuptools import setup, find_packages

# setup(
#     name='your_package',
#     version=get_version(),
#     packages=find_packages(),
#     # other setup arguments
# )