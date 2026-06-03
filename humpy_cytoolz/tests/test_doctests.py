import doctest
import humpy_cytoolz
import humpy_cytoolz.dicttoolz
import humpy_cytoolz.functoolz
import humpy_cytoolz.itertoolz
import humpy_cytoolz.recipes

def module_doctest(m, *args, **kwargs):
    return doctest.testmod(m, *args, **kwargs).failed == 0

def test_doctest():
    assert module_doctest(humpy_cytoolz)
    assert module_doctest(humpy_cytoolz.dicttoolz)
    assert module_doctest(humpy_cytoolz.functoolz)
    assert module_doctest(humpy_cytoolz.itertoolz)
    assert module_doctest(humpy_cytoolz.recipes)
