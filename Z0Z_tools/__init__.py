import configparser
from pathlib import Path
parse_setupDOTcfg = configparser.ConfigParser()
parse_setupDOTcfg.read(Path(__file__).resolve().parent.parent / 'setup.cfg')
__version__ = parse_setupDOTcfg.get('metadata', 'version', fallback='0.0.0')
__author__ = parse_setupDOTcfg.get('metadata', 'author', fallback='Unknown')

# from .pipAnything import installPackageTarget, makeListRequirementsFromRequirementsFile
from .Z0Z_io import dataTabularTOpathFilenameDelimited, getPathFilenames, loadSpectrograms, spectrogramTOpathFilenameAudio, writeWav, readAudioFile

__all__ = [
    'dataTabularTOpathFilenameDelimited', 
    'getPathFilenames', 
    # 'installPackageTarget', 
    'loadSpectrograms', 
    # 'makeListRequirementsFromRequirementsFile', 
    'readAudioFile',
    'spectrogramTOpathFilenameAudio',
    'writeWav',
           ]

