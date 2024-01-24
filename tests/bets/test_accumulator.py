from unittest import TestCase

from pybet import Odds
from pybet.bets import Accumulator


class TestAccumulator(TestCase):
    def test_accumulator_can_be_initialised_with_list_of_odds_and_events(self):
        self.assertTrue(
            Accumulator(
                2,
                [
                    [Odds(2), lambda: True],
                    [Odds(3), lambda: True],
                    [Odds(5), lambda: True],
                ],
            )
        )

    def test_accumulator_settles_as_win_if_all_bets_win(self):
        acc = Accumulator(
            2,
            [[Odds(2), lambda: True], [Odds(3), lambda: True], [Odds(5), lambda: True]],
        )
        self.assertEqual(acc.settle(), 60)

    def test_accumulator_settles_as_loss_if_any_bet_loses(self):
        acc = Accumulator(
            2,
            [
                [Odds(2), lambda: True],
                [Odds(3), lambda: False],
                [Odds(5), lambda: True],
            ],
        )
        self.assertEqual(acc.settle(), 0)