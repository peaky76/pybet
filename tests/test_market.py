from decimal import Decimal
from pybet.src.pybet import Market, Odds
from unittest import TestCase


class MarketTestCase(TestCase):

    def setUp(self):
        self.runners = ['alpha', 'beta', 'gamma', 'delta']
        self.odds = [Odds(x) for x in [2, 4, 5, 10]]
        self.place_odds = [Odds.fractional(x) for x in ['2/5', '4/5', '1', '2']]
        self.market = Market(zip(self.runners, self.odds))
        self.place_market = Market(zip(self.runners, self.place_odds))
        self.place_market.places = 2
        self.empty_market = Market.fromkeys(self.runners)

    def test_initialise_market_without_odds(self):
        self.assertEqual(self.empty_market.get('alpha'), None)

    def test_set_market_places(self):
        self.assertEqual(self.place_market.places, 2)

    def test_market_percentage(self):
        self.assertEqual(self.market.percentage, 105)

    def test_market_overround_per_runner(self):
        self.assertEqual(self.market.overround_per_runner, 1.25)

    def test_market_overround_per_runner_place_market(self):
        self.assertAlmostEqual(self.place_market.overround_per_runner, Decimal('2.579'), places=3)

    def test_market_favourites(self):
        self.assertEqual(self.market.favourites, ['alpha'])

    def test_market_is_overround(self):
        self.assertTrue(self.market.is_overround)

    def test_market_is_overround_place_market(self):
        self.assertTrue(self.place_market.is_overround)

    def test_market_is_fair(self):
        market = {'alpha': Odds(4), 'beta': Odds(4), 'gamma': Odds(4), 'delta': Odds(4)}
        self.assertTrue(Market(market).is_fair)

    def test_market_is_overbroke(self):
        market = {'alpha': Odds(4), 'beta': Odds(4), 'gamma': Odds(4), 'delta': Odds(5)}
        self.assertTrue(Market(market).is_overbroke)

    def test_market_apply_margin_positive_correctly_updates_overround(self):
        self.market.apply_margin(10)
        self.assertAlmostEqual(self.market.percentage, Decimal(110), places=0)

    def test_market_apply_margin_positive_correctly_updates_favourite(self):
        self.market.apply_margin(10)
        self.assertAlmostEqual(self.market.get('alpha'), Decimal(1.909), places=3)

    def test_market_apply_margin_positive_correctly_updates_outsider(self):
        self.market.apply_margin(10)
        self.assertAlmostEqual(self.market.get('delta'), Decimal(9.545), places=3)

    def test_market_apply_margin_negative_correctly_updates_overround(self):
        self.market.apply_margin(-10)
        self.assertAlmostEqual(self.market.percentage, Decimal(90), places=0)

    def test_market_apply_margin_negative_correctly_updates_favourite(self):
        self.market.apply_margin(-10)
        self.assertAlmostEqual(self.market.get('alpha'), Decimal(2.333), places=3)

    def test_market_apply_margin_negative_correctly_updates_outsider(self):
        self.market.apply_margin(-10)
        self.assertAlmostEqual(self.market.get('delta'), Decimal(11.667), places=3)

    def test_market_share_for(self):
        self.assertAlmostEqual(self.market.share_for('alpha'), Decimal(47.62), places=2)
  
    def test_market_without(self):
        new_market = self.market.without(['alpha', 'gamma'])
        self.assertEqual(len(new_market), 2)
        self.assertEqual(new_market.percentage, 35)
