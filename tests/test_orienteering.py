import pytest
from math import sqrt
from orienteering import euclidean_distance, CheckPoint, get_valid_number_input


class Test_euclidean_distance:
    def test_same_point_distance_zero(self):
        cp = CheckPoint(123, 10, 20)
        assert euclidean_distance(cp, cp) == 0

    def test_regular_distance(self):
        cp1 = CheckPoint(123, 0, 0)
        cp2 = CheckPoint(123, 1, 1)
        assert euclidean_distance(cp1, cp2) - sqrt(2) < 1e-5

    def test_linear_distance_x(self):
        cp1 = CheckPoint(123, 0, 0)
        cp2 = CheckPoint(123, 4, 0)
        assert euclidean_distance(cp1, cp2) - 4 < 1e-5

    def test_linear_distance_y(self):
        cp1 = CheckPoint(123, 0, 0)
        cp2 = CheckPoint(123, 0, 4)
        assert euclidean_distance(cp1, cp2) - 4 < 1e-5
    
class Test_get_valid_number_input:
    def set_stdin(self, value, monkeypatch):
        monkeypatch.setattr('builtins.input', lambda _: value)
        
    def test_valid_int_input(self, monkeypatch):
        self.set_stdin('1', monkeypatch)
        number = get_valid_number_input('')
        assert number == 1

    def test_valid_float_input(self, monkeypatch):
        self.set_stdin('1.5', monkeypatch)
        number = get_valid_number_input('')
        assert number - 1.5 < 1e-5
