from typing import Optional, Union
import multiprocessing

def defineConcurrencyLimit(limit: Optional[Union[int, float, bool]]) -> int:
    """
    Determine the concurrency limit based on the provided `limit` parameter.
    Parameters:
        limit: The concurrency limit specification. It can be
            - `None`, `False`, or `0`: Use the total number of CPUs.
            - Integer `>= 1`: Directly specifies the concurrency limit.
            - Float `0 < limit < 1`: Fraction of total CPUs to use.
            - Float `-1 < limit < 0`: Subtract a fraction of CPUs from the total.
            - Integer `<= -1`: Subtract the absolute value from total CPUs.
            - `True`: Set concurrency limit to 1.
    Returns:
        concurrencyLimit: The calculated concurrency limit, ensuring it is at least 1.
    """
    cpuTotal = multiprocessing.cpu_count()
    concurrencyLimit = cpuTotal

    if isinstance(limit, str):
        limit = oopsieKwargsie(limit) # type: ignore

    match limit:
        case None | False | 0:
            pass
        case _ if limit >= 1:
            concurrencyLimit = limit
        case _ if 0 < limit < 1:
            concurrencyLimit = int(limit * cpuTotal)
        case _ if -1 < limit < 0:
            concurrencyLimit = cpuTotal - abs(int(limit * cpuTotal))
        case _ if limit <= 1:
            concurrencyLimit = cpuTotal - abs(limit)
        case True:
            concurrencyLimit = 1

    return max(int(concurrencyLimit), 1)

def oopsieKwargsie(huh: str) -> None | str | bool:
    """
    If a calling function passes a `str` to a parameter that shouldn't receive a `str`, `oopsieKwargsie()` can might help you avoid an Exception. It tries to interpret the string as `True`, `False`, or `None`.

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

if __name__ == '__main__':
    multiprocessing.set_start_method('spawn')
