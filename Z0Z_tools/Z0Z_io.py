from typing import Iterable, Any
from os import PathLike

def dataTabularTOpathFilenameDelimited(pathFilename: PathLike, tableRows: Iterable[Iterable[Any]], tableColumns: Iterable[Any], delimiterOutput: str = '\t') -> None:
    """
    Writes tabular data to a delimited file.
    Parameters:
        pathFilename: The path and filename where the data will be written.
        tableRows: The rows of the table, where each row is a list of strings or floats.
        tableColumns: The column headers for the table.
        delimiterOutput (tab): The delimiter to use in the output file. Defaults to *tab*.
    Returns:
        None:
    """
    with open(pathFilename, 'w', newline='') as writeStream:
        writeStream.write(delimiterOutput.join(tableColumns) + '\n')
        
        for row in tableRows:
            writeStream.write(delimiterOutput.join(map(str, row)) + '\n')
