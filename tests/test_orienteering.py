from math import sqrt

import pytest
from orienteering import CheckPoint, RouteSegment, Route, euclidean_distance, get_valid_number_input, is_number


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

class Test_is_number:
    def test_valid_int(self):
        assert is_number('123') is True

    def test_valid_float(self):
        assert is_number('123.321') is True

    def test_string(self):
        assert is_number('aaa') is False


class Test_RouteSegment:
    def test_start_point_being_correctly_set(self):
        cp1 = CheckPoint(123, 0, 0)
        cp2 = CheckPoint(123, 0, 4)
        route_segment = RouteSegment(cp1, cp2)

        assert route_segment.start_check_point == cp1

    def test_end_point_being_correctly_set(self):
        cp1 = CheckPoint(123, 0, 0)
        cp2 = CheckPoint(123, 0, 4)
        route_segment = RouteSegment(cp1, cp2)

        assert route_segment.end_check_point == cp2

    def test_distance_is_zero_for_same_start_and_end(self):
        cp1 = CheckPoint(123, 0, 0)
        route_segment = RouteSegment(cp1, cp1)

        assert route_segment.distance == 0

    def test_distance_is_correct_linear_distance_x(self):
        cp1 = CheckPoint(123, 0, 0)
        cp2 = CheckPoint(123, 4, 0)
        route_segment = RouteSegment(cp1, cp2)

        assert route_segment.distance - 4 < 1e-5

    def test_distance_is_correct_linear_distance_y(self):
        cp1 = CheckPoint(123, 0, 0)
        cp2 = CheckPoint(123, 0, 4)
        route_segment = RouteSegment(cp1, cp2)

        assert route_segment.distance - 4 < 1e-5

    def test_distance_is_correct(self):
        cp1 = CheckPoint(123, 0, 0)
        cp2 = CheckPoint(123, 1, 1)
        route_segment = RouteSegment(cp1, cp2)

        assert route_segment.distance - sqrt(2) < 1e-5

class Test_Route:
    def test_starting_point_being_add_to_route(self):
        cp1 = CheckPoint(123, 0, 0)
        route = Route(cp1)

        assert len(route.check_points) == 1
        assert route.check_points[0] == cp1

    def test_get_total_distance_with_new_check_point_same_check_point(self):
        cp1 = CheckPoint(123, 0, 0)
        route = Route(cp1)

        assert route.get_total_distance_with_new_check_point(cp1) == 0

    def test_get_total_distance_with_new_check_point_linear_x(self):
        cp1 = CheckPoint(123, 0, 0)
        route = Route(cp1)

        cp2 = CheckPoint(123, 2, 0)

        assert route.get_total_distance_with_new_check_point(cp2) - 4 < 1e-5

    def test_get_total_distance_with_new_check_point_linear_y(self):
        cp1 = CheckPoint(123, 0, 0)
        route = Route(cp1)

        cp2 = CheckPoint(123, 0, 2)

        assert route.get_total_distance_with_new_check_point(cp2) - 4 < 1e-5

    def test_get_total_distance_with_new_check_point(self):
        cp1 = CheckPoint(123, 0, 0)
        route = Route(cp1)

        cp2 = CheckPoint(123, 1, 1)

        assert route.get_total_distance_with_new_check_point(cp2) - 2*sqrt(2) < 1e-5

    def test_add_check_point_starting_point_added(self):
        cp1 = CheckPoint(123, 0, 0)
        route = Route(cp1)
        route.add_check_point(cp1)

        assert len(route.check_points) == 2
        assert route.check_points[-1] == cp1

        assert route.route_distance == 0
        assert route.return_distance == 0
        assert route.total_distance == 0

    def test_add_check_point_linear_x_difference(self):
        cp1 = CheckPoint(123, 0, 0)
        cp2 = CheckPoint(321, 2, 0)
        route = Route(cp1)
        route.add_check_point(cp2)

        assert len(route.check_points) == 2
        assert route.check_points[-1] == cp2

        assert route.route_distance == 2
        assert route.return_distance == 2
        assert route.total_distance == 4

    def test_add_check_point_linear_y_difference(self):
        cp1 = CheckPoint(123, 0, 0)
        cp2 = CheckPoint(321, 0, 2)
        route = Route(cp1)
        route.add_check_point(cp2)

        assert len(route.check_points) == 2
        assert route.check_points[-1] == cp2

        assert route.route_distance == 2
        assert route.return_distance == 2
        assert route.total_distance == 4

    def test_add_check_point(self):
        cp1 = CheckPoint(123, 0, 0)
        cp2 = CheckPoint(321, 1, 1)
        route = Route(cp1)
        route.add_check_point(cp2)

        assert len(route.check_points) == 2
        assert route.check_points[-1] == cp2

        assert route.route_distance - sqrt(2) < 1e-5
        assert route.return_distance - sqrt(2) < 1e-5
        assert route.total_distance - 2*sqrt(2) < 1e-5
