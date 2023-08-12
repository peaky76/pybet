from pybet import Bet, Odds
from unittest import TestCase


class TestBet(TestCase):
    def test_bet_can_be_initialised(
        self,
    ):
        self.assertTrue(Bet(2.50, Odds(2), lambda: None, lambda: None))

    def test_is_settled_returns_true_if_end_condition_is_true_and_win_condition_is_true(
        self,
    ):
        bet = Bet(2.50, Odds(2), lambda: True, lambda: True)
        self.assertTrue(bet.is_settled)

    def test_is_settled_returns_true_if_end_condition_is_true_and_win_condition_is_false(
        self,
    ):
        bet = Bet(2.50, Odds(2), lambda: False, lambda: True)
        self.assertTrue(bet.is_settled)

    def test_is_settled_raises_error_if_end_condition_is_true_and_win_condition_is_indeterminate(
        self,
    ):
        bet = Bet(2.50, Odds(2), lambda: None, lambda: True)
        self.assertTrue(bet.is_settled)

    def test_is_settled_returns_false_if_end_condition_is_false(
        self,
    ):
        bet = Bet(2.50, Odds(2), lambda: True, lambda: False)
        self.assertFalse(bet.is_settled)

    def test_is_settled_returns_false_if_end_condition_is_undetermined(
        self,
    ):
        bet = Bet(2.50, Odds(2), lambda: True, lambda: None)
        self.assertFalse(bet.is_settled)
