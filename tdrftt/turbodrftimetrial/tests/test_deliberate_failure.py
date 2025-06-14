import pytest


@pytest.mark.skip(reason="This test needs removing in the longer term")
def test_failing():
    assert (1, 2, 3) == (3, 2, 1)
