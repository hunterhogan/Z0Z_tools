from collections.abc import Callable
from typing import ParamSpec, TypeVar
from tests.conftest import PytestFor_defineConcurrencyLimit, PytestFor_intInnit, PytestFor_oopsieKwargsie
import pytest

P = ParamSpec('P')
R = TypeVar('R')

@pytest.mark.parametrize("nameOfTest,callablePytest", PytestFor_defineConcurrencyLimit())
def testConcurrencyLimit(nameOfTest: str, callablePytest: Callable[P, R], *arguments: P.args, **keywordArguments: P.kwargs) -> None:
	callablePytest(*arguments, **keywordArguments)

@pytest.mark.parametrize("nameOfTest,callablePytest", PytestFor_intInnit())
def testIntInnit(nameOfTest: str, callablePytest: Callable[P, R], *arguments: P.args, **keywordArguments: P.kwargs) -> None:
	callablePytest(*arguments, **keywordArguments)

@pytest.mark.parametrize("nameOfTest,callablePytest", PytestFor_oopsieKwargsie())
def testOopsieKwargsie(nameOfTest: str, callablePytest: Callable[P, R], *arguments: P.args, **keywordArguments: P.kwargs) -> None:
	callablePytest(*arguments, **keywordArguments)
