from typing import Any, Collection, Dict, List, Mapping

def stringItUp(*scrapPile: Any) -> List[str]:
    """
    Recursively extracts all elements from nested data structures and converts the elements to strings.
    Order is not preserved.
    Parameters:
        *scrapPile: One or more data structures to unpack and convert to strings.
    Returns:
        listStrungUp: A list of string versions of all elements in the input data structure.
    """
    listStrungUp = []

    def drill(KitKat: Any) -> None:
        if isinstance(KitKat, str):
            listStrungUp.append(KitKat)
        elif isinstance(KitKat, (int, float, complex)):
            listStrungUp.append(str(KitKat))
        elif isinstance(KitKat, dict):
            for broken, piece in KitKat.items():
                drill(broken)
                drill(piece)
        elif isinstance(KitKat, (list, set, tuple)):
            for kit in KitKat:
                drill(kit)
        elif hasattr(KitKat, '__iter__'): # Unpack other iterables
            for kat in KitKat:
                drill(kat)
        else:
            try:
                sharingIsCaring = KitKat.__str__()
                listStrungUp.append(sharingIsCaring)
            except AttributeError:
                pass

    drill(scrapPile)
    return listStrungUp

def updateExtendPolishDictionaryLists(*dictionaryLists: Mapping[str, Collection[Any]], destroyDuplicates: bool = False, reorderLists: bool = False, killErroneousDataTypes: bool = False) -> Dict[str, List[Any]]:
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
        for keyName, keyValue in dictionaryListTarget.items():
            try:
                ImaStr = str(keyName)
                ImaList = list(keyValue)
                ePluribusUnum.setdefault(ImaStr, []).extend(ImaList)
            except TypeError:
                if killErroneousDataTypes:
                    continue
                else:
                    raise

    if destroyDuplicates:
        for ImaStr, ImaList in ePluribusUnum.items():
            ePluribusUnum[ImaStr] = list(dict.fromkeys(ImaList))
    if reorderLists:
        for ImaStr, ImaList in ePluribusUnum.items():
            ePluribusUnum[ImaStr] = sorted(ImaList)
    
    return ePluribusUnum
