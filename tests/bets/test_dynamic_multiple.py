from unittest import TestCase

from pybet import Odds
from pybet.bets import ThirteenFold  # type: ignore


class TestBet(TestCase):
    def test_dynamic_accumulator_class_up_to_twenty(self):
        with self.assertRaises(ValueError):
            ThirteenFold(
                2,
                [[Odds(2), lambda: True], [Odds(3), lambda: True]],
            ) 