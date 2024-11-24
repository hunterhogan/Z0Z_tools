"""Z0Z_tools package."""
from importlib.metadata import metadata

metadataPackage = metadata('Z0Z_tools')
__version__ = metadataPackage['Version']
__author__ = metadataPackage['Author']

from Z0Z_tools.pipAnything import installPackageTarget, makeListRequirementsFromRequirementsFile
from Z0Z_tools.Z0Z_dataStructure import stringItUp, updateExtendPolishDictionaryLists
from Z0Z_tools.Z0Z_io import dataTabularTOpathFilenameDelimited
from Z0Z_tools.Z0Z_ioAudio import writeWav, readAudioFile, loadWaveforms

__all__ = [
    'dataTabularTOpathFilenameDelimited',
    'installPackageTarget',
    'loadWaveforms',
    'makeListRequirementsFromRequirementsFile',
    'readAudioFile',
    'stringItUp',
    'updateExtendPolishDictionaryLists',
    'writeWav',
]

