import multiprocessing
from typing import Any, Callable, List, Optional, Union
from unittest.mock import patch


def defineConcurrencyLimit(limit: Optional[Union[int, float, bool]]) -> int:
    """
    Determine the concurrency limit based on the provided `limit` parameter.

    Parameters:
        limit: The concurrency limit specification. Your user can set a limit with 
        a simple True/False, a quantity of CPUs, or a ratio of CPUs. Furthermore, positive
        numbers define the maximum usage, and negative numbers define the amount to keep
        in reserve.

    Returns:
        concurrencyLimit: The calculated concurrency limit, ensuring it is at least 1.

    If you want to be extra nice to your users, consider using `oopsieKwargsie()` to handle
    malformed inputs.
    """
    """Example docstring:
    Parameters:
        CPUlimit: whether and how to limit the CPU usage. See notes for details. 

    Limits on CPU usage `CPUlimit`:
        - `False`, `None`, or `0`: No limits on CPU usage; uses all available CPUs. All other values will potentially limit CPU usage.
        - `True`: Yes, limit the CPU usage; limits to 1 CPU.
        - Integer `>= 1`: Limits usage to the specified number of CPUs.
        - Decimal value (`float`) between 0 and 1: Fraction of total CPUs to use.
        - Decimal value (`float`) between -1 and 0: Fraction of CPUs to *not* use.
        - Integer `<= -1`: Subtract the absolute value from total CPUs.
    """
    cpuTotal = multiprocessing.cpu_count()
    concurrencyLimit = cpuTotal

    if isinstance(limit, str):
        limit = oopsieKwargsie(limit) # type: ignore

    match limit:
        case None | False | 0:
            pass
        case True:
            concurrencyLimit = 1
        case _ if limit >= 1:
            concurrencyLimit = limit
        case _ if 0 < limit < 1:
            concurrencyLimit = int(limit * cpuTotal)
        case _ if -1 < limit < 0:
            concurrencyLimit = cpuTotal - abs(int(limit * cpuTotal))
        case _ if limit <= 1:
            concurrencyLimit = cpuTotal - abs(limit)

    return max(int(concurrencyLimit), 1)

def oopsieKwargsie(huh: str) -> None | str | bool:
    """
    If a calling function passes a `str` to a parameter that shouldn't receive a `str`, `oopsieKwargsie()` might help you avoid an Exception. It tries to interpret the string as `True`, `False`, or `None`.

    Parameters:
        huh: The input string to be parsed.

    Returns:
        (bool | None | str): The reserved keywords `True`, `False`, or `None` or the original string, `huh`.
    """
    formatted = huh.strip().title()
    if formatted == str(True):
        return True
    elif formatted == str(False):
        return False
    elif formatted == str(None):
        return None
    else:
        return huh

def intInnit(listInt_Allegedly: List[int], parameterName: str = 'unnamed parameter') -> List[int]:
    """
    Rigorously validates and converts input to a list of non-negative integers.
    Also returns a filtered list containing only positive integers.

    Parameters:
        listInt_Allegedly: Input that should be a list of integers
        parameterName: Name of parameter for error messages

    Returns:
        listValidated: List of integers as `int` type

    Raises:
        Various built-in Python exceptions with enhanced error messages.
    """
    if not listInt_Allegedly:
        raise ValueError(f"{parameterName} must not be empty")

    try:
        iter(listInt_Allegedly)
        lengthInitial = len(listInt_Allegedly)
        
        listValidated = []
        for allegedInt in listInt_Allegedly:
            if isinstance(allegedInt, bool):
                raise TypeError(f"Boolean values ({allegedInt}) are not integers.")
            elif isinstance(allegedInt, (int, float)):
                if float(allegedInt).is_integer():
                    allegedInt = int(allegedInt)
                else:
                    raise ValueError(f"Value {allegedInt} must be a whole number")
            else:
                raise TypeError(f"Value {allegedInt} must be numeric")
            
            listValidated.append(allegedInt)
                
            if len(listInt_Allegedly) != lengthInitial:
                raise RuntimeError("Input sequence was modified during iteration")

        return listValidated

    except TypeError as ERRORtype:
        if not hasattr(listInt_Allegedly, '__iter__'):
            ERRORmessage = f"{parameterName} does not have the '__iter__' attribute (it is not iterable), but it must have the '__iter__' attribute. Value was passed as data type '{type(listInt_Allegedly)}'."
        else:
            ERRORmessage = f"Invalid element in {parameterName}: {ERRORtype.args[0]}"
        raise TypeError(ERRORmessage) from None

if __name__ == '__main__':
    multiprocessing.set_start_method('spawn')
