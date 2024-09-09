from setuptools import setup, find_packages
from packaging.requirements import Requirement

with open('requirements.txt') as fileRequirements:
    listRequirements = [str(Requirement(requirement.strip())) for requirement in fileRequirements if requirement.strip()]

setup(
    name='Z0Z_tools',
    version='0.0.3',
    packages=find_packages(),
    install_requires=listRequirements,
    download_url='https://github.com/hunterhogan/Z0Z_tools.git',
)
