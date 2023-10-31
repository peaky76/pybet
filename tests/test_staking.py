from unittest import TestCase

from pybet import Odds
from pybet.staking import kelly


class TestStaking(TestCase):
    def test_kelly_stake_when_bettor_has_edge(self):
        self.assertEqual(6.25, kelly(Odds(4), Odds(5), 100))

    def test_kelly_stake_when_bettor_does_not_have_edge(self):
        self.assertEqual(0, kelly(Odds(5), Odds(4), 100))

    def test_kelly_stake_when_bettor_has_edge_and_commission_applied(self):
        self.assertEqual(6.25, kelly(Odds(4), Odds(6), 100, 20))

    def test_kelly_stake_raises_value_error_if_commission_is_less_than_0(self):
        with self.assertRaises(ValueError):
            kelly(Odds(4), Odds(5), 100, -1)

    def test_kelly_stake_raises_value_error_if_commission_is_greater_than_100(self):
        with self.assertRaises(ValueError):
            kelly(Odds(4), Odds(5), 100, 101)
