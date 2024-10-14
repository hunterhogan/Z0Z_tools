from pathlib import Path
from typing import List, Optional
import json
import pandas

def dataTabularTOpathFilenameDelimited(pathFilename: str, tableRows: List[List[str | float]], tableColumns: List[str], delimiterOutput: str = '\t') -> None:
    """
    Writes tabular data to a delimited file.
    This function is lame; I'll change it when I change the stuff that uses it.

    Args:
        pathFilename (str): The path to the output file.
        tableRows (List[List[Union[str, float]]]): A list of rows representing the tabular data.
        tableColumns (List[str]): A list of column names.
        delimiterOutput (str, optional): The delimiter to use. Defaults to `tab`.

    Returns:
        None
    """
    dataframeOutput = pandas.DataFrame(tableRows, columns=tableColumns)
    dataframeOutput.to_csv(pathFilename, sep=delimiterOutput, index=False)

def getPathFilenames(pathTarget: Optional[str], maskFilename: Optional[str], getMode: Optional[str] = 'mask', pathFilenameJSON: Optional[str] = None) -> List[str]:
    """Don't use this function. Use the `pathlib` module instead.

    This crappy function will either be replaced or overhauled. FYI."""
    pathTarget = Path(pathTarget) if pathTarget else Path.cwd()

    if getMode == 'mask':
        return [pathFilename.as_posix() for pathFilename in pathTarget.glob(maskFilename)]
    elif getMode == 'json':
        with open(pathFilenameJSON, 'r') as readStream:
            list_filename = [Path(item['filename']).as_posix() for item in json.load(readStream)]
        if not list_filename:
            raise ValueError(f"The JSON file {pathFilenameJSON} does not have any keys named 'filename' (case-sensitive).")
        return list_filename
    else:
        raise ValueError(f"Invalid input mode: {getMode}. Choose 'json' or 'mask'.")
