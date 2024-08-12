import sys
import os
import subprocess
import tempfile
from packaging.requirements import Requirement

"""
from path.to.Z0Z_tools.pipAnything import installPackageTarget
installPackageTarget('path/to/packageTarget')

pip will attempt to install requirements.txt, but don't rely on dependencies being installed.
"""

def make_setupDOTpy(packageTarget):
    pathPackage = os.path.abspath(packageTarget)
    listRequirements = []

    pathFilenameRequirements = os.path.join(pathPackage, 'requirements.txt')
    if os.path.exists(pathFilenameRequirements):
        fileRequirements = open(pathFilenameRequirements, 'r')
        listRequirements = [str(Requirement(requirement.strip())) for requirement in fileRequirements if requirement.strip()]
        fileRequirements.close()

    return f"""
import os
from setuptools import setup, find_packages

setup(
    name='{os.path.basename(pathPackage)}',
    version='0.0.0',
    packages=find_packages(where='{pathPackage}'),
    package_dir={{'': '{pathPackage}'}},
    install_requires={listRequirements},
    include_package_data=True,
)
"""

def installPackageTarget(packageTarget):
    systemTemporaryDirectory = tempfile.mkdtemp()

    pathFilename_setupDOTpy = os.path.join(systemTemporaryDirectory, 'setup.py')
    fileOut = open(pathFilename_setupDOTpy, 'w')
    fileOut.write(make_setupDOTpy(packageTarget))
    fileOut.close()

    subprocessPython = subprocess.Popen(
        [sys.executable, '-m', 'pip', 'install', systemTemporaryDirectory],
        stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)

    for lineStdout in subprocessPython.stdout:
        print(lineStdout, end="")

    subprocessPython.wait()

    os.remove(pathFilename_setupDOTpy)

def everyone_knows_what___main___is():
    packageTarget = sys.argv[1] if len(sys.argv) > 1 else ''
    if not os.path.isdir(packageTarget) or len(sys.argv) != 2:
        print(f"\n{(namespaceModule:=os.path.splitext(os.path.basename(__file__))[0])} says, 'That didn't work. Try again?'\n"
            f"Usage:\tpython -m {(namespacePackage:=os.path.basename(os.path.dirname(__file__)))}.{namespaceModule} '<packageTarget>'\n"
              f"\t<packageTarget> is a path to a directory with Python modules\n"
              f"\tExample: python -m {namespacePackage}.{namespaceModule} '{os.path.join('.', 'Z0Z_tools')}'") # os.path.join for platform-independent path separator
        # What is `-m`? Obviously, `-m` creates a namespace for the module, which is obviously necessary, except when it isn't.
        sys.exit(1)

    installPackageTarget(packageTarget)
    print(f"{__name__.split('.')[-1]} finished trying to trick pip into installing {os.path.basename(packageTarget)}")

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
