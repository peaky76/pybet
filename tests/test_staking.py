from pybet import Odds
from pybet.staking import kelly
from unittest import TestCase


class TestStaking(TestCase):
    def test_kelly_stake_when_bettor_has_edge(self):
        self.assertEqual(6.25, kelly(Odds(4), Odds(5), 100))

    def test_kelly_stake_when_bettor_does_not_have_edge(self):
        self.assertEqual(0, kelly(Odds(5), Odds(4), 100))
