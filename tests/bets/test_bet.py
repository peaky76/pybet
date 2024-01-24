from unittest import TestCase

from pybet import Odds
from pybet.bets import Bet


class TestBet(TestCase):
    def test_bet_can_be_initialised_with_all_params(
        self,
    ):
        self.assertTrue(Bet(2.50, Odds(2), lambda: None, lambda: None))

    def test_bet_can_be_initialised_with_default_end_condition_as_true(
        self,
    ):
        bet = Bet(2.50, Odds(2), lambda: None)
        self.assertTrue(bet.end_condition())

    def test_bet_can_be_initialised_with_sp(
        self,
    ):
        self.assertTrue(Bet(2.50, "SP", lambda: None, lambda: None))

    def test_bet_raises_value_error_if_initialised_with_string_other_than_sp(
        self,
    ):
        with self.assertRaises(ValueError):
            Bet(2.50, "foobar", lambda: None, lambda: None)

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

    def test_bet_settle_raises_error_if_sp_not_set(self):
        bet = Bet(2.50, "SP", lambda: True, lambda: True)
        with self.assertRaises(ValueError):
            bet.settle()

    def test_bet_settle_returns_stake_times_sp_if_sp_given_in_call(self):
        bet = Bet(2.50, "SP", lambda: True, lambda: True)
        self.assertEqual(bet.settle(sp=Odds(2)), 5)

    def test_bet_settle_returns_correct_value_if_reduction_applied(self):
        bet = Bet(2.50, Odds(2), lambda: True, lambda: True)
        self.assertEqual(bet.settle(rf=10), 4.75)

    def test_bet_settle_returns_correct_value_if_bog_and_sp_higher(self):
        bet = Bet(2.50, Odds(2), lambda: True, bog=True)
        self.assertEqual(bet.settle(sp=Odds(3)), 7.50)

    def test_bet_settle_returns_correct_value_if_bog_and_sp_lower(self):
        bet = Bet(2.50, Odds(3), lambda: True, bog=True)
        self.assertEqual(bet.settle(sp=Odds(2)), 7.50)

    def test_bet_settle_returns_correct_value_if_sp_taken_but_bog_set(self):
        bet = Bet(2.50, "SP", lambda: True, bog=True)
        self.assertEqual(bet.settle(sp=Odds(2)), 5.00)

    def test_bet_settle_raises_error_if_bog_but_sp_not_given(self):
        bet = Bet(2.50, Odds(2), lambda: True, bog=True)
        with self.assertRaises(ValueError):
            bet.settle()

    def test_bet_settle_raises_error_if_reduction_factor_is_gte_100(self):
        bet = Bet(2.50, Odds(2), lambda: True, lambda: True)
        with self.assertRaises(ValueError):
            bet.settle(rf=110)

    def test_bet_settle_raises_error_if_reduction_factor_is_lt_0(self):
        bet = Bet(2.50, Odds(2), lambda: True, lambda: True)
        with self.assertRaises(ValueError):
            bet.settle(rf=-0.1)

    def test_bet_settle_raises_error_if_bet_market_is_not_ended(self):
        bet = Bet(2.50, Odds(2), lambda: True, lambda: False)
        with self.assertRaises(ValueError):
            bet.settle()

    def test_bet_status_returns_open_if_bet_market_is_not_ended(self):
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

