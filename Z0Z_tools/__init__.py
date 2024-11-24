__author__ = "Hunter Hogan"
__url__ = "https://github.com/hunterhogan/Z0Z_tools"
__version__ = "0.5.2"
__dependencies__ = [
    "numpy",
    "packaging",
    "samplerate @ git+https://github.com/tuxu/python-samplerate.git@fix_cmake_dep ; platform_system == 'Linux' and platform_machine == 'x86_64' and python_version <= '3.10'",
    "samplerate",
    "soundfile"
]

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

