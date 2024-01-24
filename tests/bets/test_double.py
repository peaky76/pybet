from unittest import TestCase

from pybet import Odds
from pybet.bets import Double


class TestDouble(TestCase):
    def test_double_raises_error_if_not_correct_number_of_selections(self):
        with self.assertRaises(ValueError):
            Double(
                2,
                [
                    [Odds(2), lambda: True],
                    [Odds(3), lambda: True],
                    [Odds(5), lambda: True],
                ],
            )
