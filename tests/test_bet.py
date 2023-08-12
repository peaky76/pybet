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

    def test_bet_returns_is_stake_times_odds_if_bet_is_won(self):
        bet = Bet(2.50, Odds(2), lambda: True, lambda: True)
        self.assertEqual(bet.returns, 5)

    def test_bet_returns_is_zero_if_bet_is_lost(self):
        bet = Bet(2.50, Odds(2), lambda: False, lambda: True)
        self.assertEqual(bet.returns, 0)

    def test_bet_returns_raises_error_if_bet_is_not_settled(self):
        bet = Bet(2.50, Odds(2), lambda: True, lambda: False)
        with self.assertRaises(ValueError):
            bet.returns

    def test_bet_status_returns_open_if_bet_is_not_settled(self):
        bet = Bet(2.50, Odds(2), lambda: True, lambda: False)
        self.assertEqual(str(bet.status), "OPEN")

    def test_bet_status_returns_win_if_bet_settled_and_win_condition_is_true(self):
        bet = Bet(2.50, Odds(2), lambda: True, lambda: True)
        self.assertEqual(str(bet.status), "WON")

    def test_bet_status_returns_lost_if_bet_settled_and_win_condition_is_false(self):
        bet = Bet(2.50, Odds(2), lambda: False, lambda: True)
        self.assertEqual(str(bet.status), "LOST")
