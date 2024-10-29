import configparser
from pathlib import Path
parse_setupDOTcfg = configparser.ConfigParser()
parse_setupDOTcfg.read(Path(__file__).resolve().parent.parent / 'setup.cfg')
__version__ = parse_setupDOTcfg.get('metadata', 'version', fallback='0.0.0')
__author__ = parse_setupDOTcfg.get('metadata', 'author', fallback='Unknown')

from Z0Z_tools.pipAnything import installPackageTarget, makeListRequirementsFromRequirementsFile
from Z0Z_tools.Z0Z_dataStructure import updateExtendPolishDictionaryLists
from Z0Z_tools.Z0Z_io import dataTabularTOpathFilenameDelimited
from Z0Z_tools.Z0Z_ioAudio import writeWav, readAudioFile, loadWaveforms

__all__ = [
    'dataTabularTOpathFilenameDelimited', 
    'installPackageTarget', 
    'loadWaveforms', 
    'makeListRequirementsFromRequirementsFile', 
    'readAudioFile',
    'updateExtendPolishDictionaryLists',
    'writeWav',
]

