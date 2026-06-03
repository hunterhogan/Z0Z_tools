import humpy_toolz

def test_has_version() -> None:
    version = humpy_toolz.__version__
    assert isinstance(version, str)
    assert version.startswith('1.')
