"""
Functions:
    - installPackageTarget: Tries to trick pip into installing the package from a given directory.
    - makeListRequirementsFromRequirementsFile: Reads a requirements.txt file, discards anything it couldn't understand, and creates a list of packages. 

Usage:
    from pipAnything import installPackageTarget
    installPackageTarget('path/to/packageTarget')

    pip will attempt to install requirements.txt, but don't rely on dependencies being installed.
"""

from os import PathLike
from packaging.requirements import Requirement
from pathlib import Path, PurePath
import subprocess
import sys
import tempfile

def makeListRequirementsFromRequirementsFile(*pathFilenames: str|PathLike) -> list[str]:
    """
    Reads one or more requirements files and extracts valid package requirements.
    Parameters:
        *pathFilenames: One or more paths to requirements files.
    Returns:
        listRequirements: A list of unique, valid package requirements found in the provided files.
    The function performs the following steps:
    1. Iterates over each provided file path.
    2. Checks if the file exists.
    3. Reads the file line by line, removing comments and trimming whitespace.
    4. Skips lines that are empty or contain spaces/tabs after sanitization.
    5. Validates if the sanitized line is a valid requirement.
    6. Collects valid requirements and removes duplicates before returning the list.
    """
    listRequirements = []
    
    for pathFilename in pathFilenames:
        if Path(pathFilename).exists():
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

    return list(set(listRequirements))  # Remove duplicates

def make_setupDOTpy(relativePathPackage: str|PathLike, listRequirements: list[str]) -> str:
    """
    Generates setup.py file content for installing the package.

    Parameters:
        relativePathPackage: The relative path to the package directory.
        listRequirements: A list of requirements to be included in install_requires.

    Returns:
        str: The setup.py content to be written to a file.
    """
    return rf"""
import os
from setuptools import setup, find_packages

setup(
    name='{Path(relativePathPackage).name}',
    version='0.0.0',
    packages=find_packages(where=r'{relativePathPackage}'),
    package_dir={{'': r'{relativePathPackage}'}},
    install_requires={listRequirements},
    include_package_data=True,
)
""" 

def installPackageTarget(packageTarget: str|PathLike) -> None:
    """
    Installs a package by creating a temporary setup.py and tricking pip into installing it.

    Parameters:
        packageTarget: The directory path of the package to be installed.
    """
    filenameRequirementsHARDCODED = Path('requirements.txt')
    filenameRequirements = Path(filenameRequirementsHARDCODED)

    pathPackage = Path(packageTarget).resolve()
    pathSystemTemporary = Path(tempfile.mkdtemp())
    pathFilename_setupDOTpy = pathSystemTemporary / 'setup.py'

    pathFilenameRequirements = pathPackage / filenameRequirements
    listRequirements = makeListRequirementsFromRequirementsFile(pathFilenameRequirements)

    # Try-finally block for file handling: with-as doesn't always work
    writeStream = None
    try:
        writeStream = pathFilename_setupDOTpy.open(mode='w')
        relativePathPackage = pathPackage.relative_to(pathSystemTemporary, walk_up=True).as_posix()
        writeStream.write(make_setupDOTpy(relativePathPackage, listRequirements))
    finally:
        if writeStream:
            writeStream.close()

    # Run pip to install the package from the temporary directory
    subprocessPython = subprocess.Popen(
    # `pip` needs a RELATIVE PATH, not an absolute path, and not a path+filename. 
        args=[sys.executable, '-m', 'pip', 'install', str(pathSystemTemporary)],
        stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True
    )

    # Output the subprocess stdout in real-time
    if subprocessPython.stdout:
        for lineStdout in subprocessPython.stdout:
            print(lineStdout, end="")

    subprocessPython.wait()

    # Clean up by removing setup.py
    pathFilename_setupDOTpy.unlink()


def everyone_knows_what___main___is() -> None:
    """A rudimentary CLI for the module.
    call `installPackageTarget` from other modules."""
    packageTarget = sys.argv[1] if len(sys.argv) > 1 else ''
    if not Path(packageTarget).is_dir() or len(sys.argv) != 2:
        namespaceModule = Path(__file__).stem
        namespacePackage = Path(__file__).parent.stem
        print(f"\n{namespaceModule} says, 'That didn't work. Try again?'\n\n"
              f"Usage:\tpython -m {namespacePackage}.{namespaceModule} <packageTarget>\n"
              f"\t<packageTarget> is a path to a directory with Python modules\n"
              f"\tExample: python -m {namespacePackage}.{namespaceModule} '{PurePath('path' ,'to', 'Z0Z_tools')}'") 
        # What is `-m`? Obviously, `-m` creates a namespace for the module, which is obviously necessary, except when it isn't.
        sys.exit(1)

    installPackageTarget(packageTarget)
    print(f"\n{Path(__file__).stem} finished trying to trick pip into installing {Path(packageTarget).name}. Did it work?")

def readability_counts() -> None:
    """Brings the snark."""
    everyone_knows_what___main___is()

def main() -> None:
    """Jabs subtly."""
    readability_counts()

if __name__ == "__main__":
    main()