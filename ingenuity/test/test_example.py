import pytest

class Test_Class(object):
    def func(self, x):
        return x + 1


    def test_func(self):
        assert self.func(3) == 5
