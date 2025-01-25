from tests.conftest import *
import pytest

@pytest.mark.parametrize("nameOfTest,callablePytest", PytestFor_defineConcurrencyLimit())
def testConcurrencyLimit(nameOfTest, callablePytest):
    callablePytest()

@pytest.mark.parametrize("nameOfTest,callablePytest", PytestFor_intInnit())
def testIntInnit(nameOfTest, callablePytest):
    callablePytest()

@pytest.mark.parametrize("nameOfTest,callablePytest", PytestFor_oopsieKwargsie())
def testOopsieKwargsie(nameOfTest, callablePytest):
    callablePytest()
