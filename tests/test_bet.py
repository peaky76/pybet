from unittest import TestCase

from pybet import Bet, Odds


class TestBet(TestCase):
    def test_bet_can_be_initialised(
        self,
    ):
        self.assertTrue(Bet(2.50, Odds(2), lambda: None, lambda: None))

    def test_bet_settle_returns_stake_times_odds_if_bet_is_won(self):
        bet = Bet(2.50, Odds(2), lambda: True, lambda: True)
        self.assertEqual(bet.settle(), 5)

    def test_bet_settle_returns_zero_if_bet_is_lost(self):
        bet = Bet(2.50, Odds(2), lambda: False, lambda: True)
        self.assertEqual(bet.settle(), 0)

    def test_bet_settle_returns_stake_if_bet_is_void(self):
        bet = Bet(2.50, Odds(2), lambda: False, lambda: True)
        bet.void()
        self.assertEqual(bet.settle(), 2.50)

    def test_bet_settle_raises_error_if_bet_is_not_settled(self):
        bet = Bet(2.50, Odds(2), lambda: True, lambda: False)
        with self.assertRaises(ValueError):
            bet.settle()

    def test_bet_status_returns_open_if_bet_is_not_settled(self):
        bet = Bet(2.50, Odds(2), lambda: True, lambda: False)
        self.assertEqual(str(bet.status), "OPEN")

    def test_bet_status_returns_win_if_bet_settled_and_win_condition_is_true(self):
        bet = Bet(2.50, Odds(2), lambda: True, lambda: True)
        self.assertEqual(str(bet.status), "WON")

    def test_bet_status_returns_lost_if_bet_settled_and_win_condition_is_false(self):
        bet = Bet(2.50, Odds(2), lambda: False, lambda: True)
        self.assertEqual(str(bet.status), "LOST")

    def test_bet_void_voids_bet(self):
        bet = Bet(2.50, Odds(2), lambda: False, lambda: True)
        bet.void()
        self.assertEqual(str(bet.status), "VOID")
