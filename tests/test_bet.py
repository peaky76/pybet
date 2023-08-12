from pybet import Bet
from unittest import TestCase


class TestBet(TestCase):
    def test_bet_can_be_initialised_with_win_condition_and_end_condition_callbacks(
        self,
    ):
        self.assertTrue(Bet(lambda: None, lambda: None))
