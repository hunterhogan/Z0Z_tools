from typing import Dict, Any, List, Union
import numpy
import numpy.typing

def updateExtendPolishDictionaryLists(*dictionaryLists: Dict[str, List[Any]], destroyDuplicates: bool = False, ignoreListOrdering: bool = False, killErroneousDataTypes: bool = False) -> Dict[str, List[Any]]:
    """
    Merges multiple dictionaries containing lists into a single dictionary, with options to handle duplicates, list ordering, and erroneous data types.
    Parameters:
        *dictionaryLists: Variable number of dictionaries to be merged. If only one dictionary is passed, it will be processed based on the provided options.
        destroyDuplicates (False): If True, removes duplicate elements from the lists. Defaults to False.
        ignoreListOrdering (False): If True, sorts the lists. Defaults to False.
        killErroneousDataTypes (False): If True, skips lists that cause a TypeError during merging. Defaults to False.
    Returns:
        dictionaryLists: A single dictionary with merged lists based on the provided options. If only one dictionary is passed, it will be cleaned up based on the options.
    """

    ePluribusUnum: Dict[str, List[Any]] = {}

    for dictionaryListTarget in dictionaryLists:
        for keyName, ImaList in dictionaryListTarget.items():
            ImaList = list(ImaList)
            try:
                ePluribusUnum.setdefault(keyName, []).extend(ImaList)
            except TypeError:
                if killErroneousDataTypes:
                    continue
                else:
                    raise

    for keyName, ImaList in ePluribusUnum.items():
        if destroyDuplicates and ignoreListOrdering:
            ePluribusUnum[keyName] = list(set(ImaList))
        elif ignoreListOrdering:
            ePluribusUnum[keyName] = sorted(ImaList)
        elif destroyDuplicates:
            ePluribusUnum[keyName] = list(dict.fromkeys(ImaList))
    
    return ePluribusUnum