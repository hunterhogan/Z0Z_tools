"""
Functions:
    - installPackageTarget: Tries to trick pip into installing the package from a given directory.
    - makeListRequirementsFromRequirementsFile: Reads a requirements.txt file, discards anything it couldn't understand, and creates a list of packages. 

Usage:
    from Z0Z_tools.pipAnything import installPackageTarget
    installPackageTarget('path/to/packageTarget')

    pip will attempt to install requirements.txt, but don't rely on dependencies being installed.
"""

from packaging.requirements import Requirement
from os import PathLike
import os
import pathlib
import subprocess
import sys
import tempfile

def makeListRequirementsFromRequirementsFile(pathFilename: PathLike) -> list[str]:
    """
    Creates a list of valid package names from the provided requirements file.

    Args:
        pathFilename (PathLike): Location of a requirements file, e.g., requirements.txt.

    Returns:
        list[str]: A list of packages.
    """
    listRequirements = []
    

    if os.path.exists(pathFilename):
        try:
            filesystemObjectRead = open(pathFilename, 'r')
            for commentedLine in filesystemObjectRead:
                sanitizedLine = commentedLine.split('#')[0].strip()  # Remove comments and trim whitespace

                # Skip lines that are empty or contain spaces/tabs after sanitization
                if "\t" in sanitizedLine or " " in sanitizedLine or not sanitizedLine:
                    continue

                # Validate if it's a valid requirement
                try:
                    Requirement(sanitizedLine)
                    listRequirements.append(sanitizedLine)
                except:
                    pass  # Skip invalid requirement lines
        finally:
            filesystemObjectRead.close()

    return listRequirements


def make_setupDOTpy(relativePathPackage: PathLike) -> str:
    """
    Generates setup.py file content for installing the package.

    Args:
        relativePathPackage (str): The relative path to the package directory.

    Returns:
        str: The setup.py content to be written to a file.
    """
    filenameRequirementsHARDCODED: str = 'requirements.txt'
    filenameRequirements: str = filenameRequirementsHARDCODED
    relativePathFilenameRequirements = os.path.join(relativePathPackage, filenameRequirements)
    listRequirements = makeListRequirementsFromRequirementsFile(relativePathFilenameRequirements)
    return rf"""
import os
from setuptools import setup, find_packages

setup(
    name='{os.path.basename(relativePathPackage)}',
    version='0.0.0',
    packages=find_packages(where=r'{relativePathPackage}'),
    package_dir={{'': r'{relativePathPackage}'}},
    install_requires={listRequirements},
    include_package_data=True,
)
""" 


def installPackageTarget(packageTarget: PathLike):
    """
    Installs a package by creating a temporary setup.py and tricking pip into installing it.

    Args:
        packageTarget (str): The directory path of the package to be installed.
    """
    pathPackage = pathlib.Path(packageTarget).resolve()
    pathSystemTemporary = pathlib.Path(tempfile.mkdtemp())
    pathFilename_setupDOTpy = pathSystemTemporary / 'setup.py'

    # Try-finally block for file handling
    filesystemObjectWrite = None
    try:
        filesystemObjectWrite = pathFilename_setupDOTpy.open('w')
        relativePathPackage = pathPackage.relative_to(pathSystemTemporary).as_posix()
        filesystemObjectWrite.write(make_setupDOTpy(relativePathPackage))
    finally:
        if filesystemObjectWrite:
            filesystemObjectWrite.close()

    # Run pip to install the package from the temporary directory
    subprocessPython = subprocess.Popen(
    # `pip` needs a RELATIVE PATH, not an absolute path, and not a path+filename. 
        [sys.executable, '-m', 'pip', 'install', str(pathSystemTemporary)],
        stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True
    )

    # Output the subprocess stdout in real-time
    for lineStdout in subprocessPython.stdout:
        print(lineStdout, end="")

    subprocessPython.wait()

    # Clean up by removing setup.py
    pathFilename_setupDOTpy.unlink()


def everyone_knows_what___main___is():
    """Handles command-line arguments and installs the package."""
    packageTarget = sys.argv[1] if len(sys.argv) > 1 else ''
    if not os.path.isdir(packageTarget) or len(sys.argv) != 2:
        print(f"\n{(namespaceModule:=os.path.splitext(os.path.basename(__file__))[0])} says, 'That didn't work. Try again?'\n"
            f"Usage:\tpython -m {(namespacePackage:=os.path.basename(os.path.dirname(__file__)))}.{namespaceModule} '<packageTarget>'\n"
              f"\t<packageTarget> is a path to a directory with Python modules\n"
              f"\tExample: python -m {namespacePackage}.{namespaceModule} '{os.path.join('.', 'Z0Z_tools')}'") # os.path.join for platform-independent path separator
        # What is `-m`? Obviously, `-m` creates a namespace for the module, which is obviously necessary, except when it isn't.
        sys.exit(1)

    installPackageTarget(packageTarget)
    print(f"\n{os.path.splitext(os.path.basename(__file__))[0]} finished trying to trick pip into installing {os.path.basename(packageTarget)}. Did it work?")

def readability_counts():
    everyone_knows_what___main___is()

def main_mainly():
    readability_counts()

def mainly():
    main_mainly()

def main():
    mainly()

if __name__ == "__main__":
    main()
