from Z0Z_tools.parseParameters import defineConcurrencyLimit, oopsieKwargsie, intInnit
from Z0Z_tools.pytest_parseParameters import (
    makeTestSuiteOopsieKwargsie,
    makeTestSuiteConcurrencyLimit,
    makeTestSuiteIntInnit
)

def testOopsieKwargsie():
    dictionaryTests = makeTestSuiteOopsieKwargsie(oopsieKwargsie)
    for testName, testFunction in dictionaryTests.items():
        testFunction()

def testConcurrencyLimitGenerated():
    dictionaryTests = makeTestSuiteConcurrencyLimit(defineConcurrencyLimit)
    for testName, testFunction in dictionaryTests.items():
        testFunction()

def testIntInnitGenerated():
    dictionaryTests = makeTestSuiteIntInnit(intInnit)
    for testName, testFunction in dictionaryTests.items():
        testFunction()
