from pathlib import Path
from typing import List, Optional
import json

def dataTabularTOpathFilenameDelimited(pathFilename: str, tableRows: List[List[str | float]], tableColumns: List[str], delimiterOutput: str = '\t') -> None:
    """
    Writes tabular data to a delimited file.
    Parameters:
        pathFilename (str): The path and filename where the data will be written.
        tableRows (List[List[str | float]]): The rows of the table, where each row is a list of strings or floats.
        tableColumns (List[str]): The column headers for the table.
        delimiterOutput (str, optional): The delimiter to use in the output file. Defaults to '\t'.
    Returns:
        None:
    """
    with open(pathFilename, 'w', newline='') as writeStream:
        writeStream.write(delimiterOutput.join(tableColumns) + '\n')
        
        for row in tableRows:
            writeStream.write(delimiterOutput.join(map(str, row)) + '\n')

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
