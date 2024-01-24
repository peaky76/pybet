from unittest import TestCase

from pybet import Odds
from pybet.bets import Treble

class TestTreble(TestCase):
    def test_treble_raises_error_if_not_correct_number_of_selections(self):
        with self.assertRaises(ValueError):
            Treble(
                2,
                [[Odds(2), lambda: True], [Odds(3), lambda: True]],
            )