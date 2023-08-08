from decimal import Decimal
from pybet import Market, Odds
from unittest import TestCase


class MarketTestCase(TestCase):
    def setUp(self):
        self.runners = [
            "alpha_ace",
            "beta_boy",
            "gamma_gal",
            "delta_dame",
            "epsilon_elf",
            "zeta_zombie",
        ]
        self.odds = [Odds(x) for x in [2, 3, 5, 10, 20, 50]]
        self.place_odds = [
            Odds.fractional(x) for x in ["1/4", "1/2", "1/1", "9/4", "19/4", "49/4"]
        ]
        self.market = Market(zip(self.runners, self.odds))
        self.place_market = Market(zip(self.runners, self.place_odds))
        self.place_market.places = 2
        self.empty_market = Market.fromkeys(self.runners)
        self.discounts = [1, 0.76, 0.62, 0.5, 0.4]

    def test_initialise_market_without_odds(self):
        self.assertEqual(self.empty_market.get("alpha_ace"), None)

    def test_market_setattr_with_non_odds_instance(self):
        self.empty_market["alpha_ace"] = 2
        self.assertEqual(self.empty_market.get("alpha_ace"), Odds(2))

    def test_set_market_places(self):
        self.assertEqual(self.place_market.places, 2)

    def test_market_percentage(self):
        self.assertAlmostEqual(self.market.percentage, Decimal("120.333"), places=3)

    def test_market_overround_per_runner(self):
        self.assertAlmostEqual(
            self.market.overround_per_runner, Decimal("3.389"), places=3
        )

    def test_market_overround_per_runner_place_market(self):
        self.assertAlmostEqual(
            self.place_market.overround_per_runner, Decimal("8.729"), places=3
        )

    def test_market_favourites(self):
        self.assertEqual(self.market.favourites, ["alpha_ace"])

    def test_market_is_overround(self):
        self.assertTrue(self.market.is_overround)

    def test_market_is_overround_place_market(self):
        self.assertTrue(self.place_market.is_overround)

    def test_market_is_fair(self):
        market = {
            "alpha_ace": Odds(4),
            "beta_boy": Odds(4),
            "gamma_gal": Odds(4),
            "delta_dame": Odds(4),
        }
        self.assertTrue(Market(market).is_fair)

    def test_market_is_overbroke(self):
        market = {
            "alpha_ace": Odds(4),
            "beta_boy": Odds(4),
            "gamma_gal": Odds(4),
            "delta_dame": Odds(5),
        }
        self.assertTrue(Market(market).is_overbroke)

    def test_market_apply_margin_positive_correctly_updates_overround(self):
        self.market.apply_margin(10)
        self.assertAlmostEqual(self.market.percentage, Decimal(110), places=0)

    def test_market_apply_margin_positive_correctly_updates_favourite(self):
        self.market.apply_margin(10)
        self.assertAlmostEqual(self.market.get("alpha_ace"), Decimal(2.188), places=3)

    def test_market_apply_margin_positive_correctly_updates_outsider(self):
        self.market.apply_margin(10)
        self.assertAlmostEqual(
            self.market.get("zeta_zombie"), Decimal(54.697), places=3
        )

    def test_market_apply_margin_negative_correctly_updates_overround(self):
        self.market.apply_margin(-10)
        self.assertAlmostEqual(self.market.percentage, Decimal(90), places=0)

    def test_market_apply_margin_negative_correctly_updates_favourite(self):
        self.market.apply_margin(-10)
        self.assertAlmostEqual(self.market.get("alpha_ace"), Decimal(2.674), places=3)

    def test_market_apply_margin_negative_correctly_updates_outsider(self):
        self.market.apply_margin(-10)
        self.assertAlmostEqual(
            self.market.get("zeta_zombie"), Decimal(66.852), places=3
        )

    def test_market_derive_returns_200_percent_market_for_two_places_standard(self):
        self.assertAlmostEqual(
            Decimal("200.000"), self.market.derive(2).percentage, places=3
        )

    def test_market_derive_returns_300_percent_market_for_three_places_standard(self):
        self.assertAlmostEqual(
            Decimal("300.000"), self.market.derive(3).percentage, places=3
        )

    def test_market_derive_returns_400_percent_market_for_four_places_standard(self):
        self.assertAlmostEqual(
            Decimal("400.000"), self.market.derive(4).percentage, places=3
        )

    def test_market_derive_returns_500_percent_market_for_five_places_standard(self):
        self.assertAlmostEqual(
            Decimal("500.000"), self.market.derive(5).percentage, places=3
        )

    def test_market_derive_returns_200_percent_market_for_two_places_discounted(self):
        self.assertAlmostEqual(
            Decimal("200.000"),
            self.market.derive(2, discounts=self.discounts).percentage,
            places=3,
        )

    def test_market_derive_returns_300_percent_market_for_three_places_discounted(self):
        self.assertAlmostEqual(
            Decimal("300.000"),
            self.market.derive(3, discounts=self.discounts).percentage,
            places=3,
        )

    def test_market_derive_returns_400_percent_market_for_four_places_discounted(self):
        self.assertAlmostEqual(
            Decimal("400.000"),
            self.market.derive(4, discounts=self.discounts).percentage,
            places=3,
        )

    def test_market_derive_returns_500_percent_market_for_five_places_discounted(self):
        self.assertAlmostEqual(
            Decimal("500.000"),
            self.market.derive(5, discounts=self.discounts).percentage,
            places=3,
        )

    def test_market_derive_default_same_as_harville_discount_of_one(self):
        default = Market(self.market).derive(3)
        discounted = Market(self.market).derive(3, discounts=[1, 1, 1])
        for h in self.market.keys():
            self.assertAlmostEqual(default[h], discounted[h], places=2)

    def test_market_derive_raises_index_error_when_discounts_are_too_short(self):
        with self.assertRaises(IndexError):
            self.market.derive(3, discounts=[1, 1])

    def test_market_equalise(self):
        self.market.equalise()
        self.assertAlmostEqual(self.market.get("alpha_ace"), 6, places=0)

    def test_market_fill_assigns_correct_value_to_missing_odds_with_default_margin(
        self,
    ):
        market = Market({"alpha_ace": Odds(3), "beta_boy": Odds(3), "gamma_gal": None})
        market.fill()
        self.assertAlmostEqual(market.get("gamma_gal"), Decimal(3), places=0)

    def test_market_fill_assigns_correct_value_to_missing_odds_with_specified_margin(
        self,
    ):
        market = Market({"alpha_ace": Odds(3), "beta_boy": Odds(3), "gamma_gal": None})
        market.fill(10)
        self.assertAlmostEqual(market.get("gamma_gal"), Decimal(2.308), places=3)

    def test_market_fill_raises_error_when_specified_margin_already_exceeded(self):
        market = Market({"alpha_ace": Odds(2), "beta_boy": Odds(2), "gamma_gal": None})
        with self.assertRaises(ValueError):
            market.fill(-1)

    def test_market_meld_combines_markets_in_equal_proportion_by_default(self):
        runners = ["alpha_ace", "beta_boy", "gamma_gal"]
        market_1 = Market(zip(runners, [Odds.percentage(x) for x in (40, 30, 30)]))
        market_2 = Market(zip(runners, [Odds.percentage(x) for x in (30, 30, 40)]))
        new_market = market_1.meld(market_2)
        self.assertAlmostEqual(
            new_market.get("alpha_ace").to_percentage(), 35, places=3
        )
        self.assertAlmostEqual(new_market.get("beta_boy").to_percentage(), 30, places=3)
        self.assertAlmostEqual(
            new_market.get("gamma_gal").to_percentage(), 35, places=3
        )

    def test_market_meld_combines_markets_in_unequal_proportion_when_specified(self):
        runners = ["alpha_ace", "beta_boy", "gamma_gal"]
        market_1 = Market(zip(runners, [Odds.percentage(x) for x in (40, 30, 30)]))
        market_2 = Market(zip(runners, [Odds.percentage(x) for x in (30, 30, 40)]))
        new_market = market_1.meld(market_2, 75)
        self.assertAlmostEqual(
            new_market.get("alpha_ace").to_percentage(), Decimal(32.5), places=3
        )
        self.assertAlmostEqual(new_market.get("beta_boy").to_percentage(), 30, places=3)
        self.assertAlmostEqual(
            new_market.get("gamma_gal").to_percentage(), Decimal(37.5), places=3
        )

    def test_market_meld_combines_markets_at_100_percent_values(self):
        runners = ["alpha_ace", "beta_boy", "gamma_gal"]
        market_1 = Market(zip(runners, [Odds.percentage(x) for x in (40, 30, 30)]))
        market_2 = Market(zip(runners, [Odds.percentage(x) for x in (45, 45, 60)]))
        new_market = market_1.meld(market_2)
        self.assertAlmostEqual(
            new_market.get("alpha_ace").to_percentage(), 35, places=3
        )
        self.assertAlmostEqual(new_market.get("beta_boy").to_percentage(), 30, places=3)
        self.assertAlmostEqual(
            new_market.get("gamma_gal").to_percentage(), 35, places=3
        )

    def test_market_meld_raises_error_when_runners_missing(self):
        market_1 = Market(
            {"alpha_ace": Odds(3), "beta_boy": Odds(3), "gamma_gal": Odds(3)}
        )
        market_2 = Market({"alpha_ace": Odds(3), "beta_boy": Odds(3)})
        with self.assertRaises(ValueError):
            market_1.meld(market_2)

    def test_market_meld_raises_error_when_runners_are_not_identical(self):
        market_1 = Market(
            {"alpha_ace": Odds(3), "beta_boy": Odds(3), "gamma_gal": Odds(3)}
        )
        market_2 = Market(
            {"alpha_ace": Odds(3), "beta_boy": Odds(3), "delta_dame": Odds(3)}
        )
        with self.assertRaises(ValueError):
            market_1.meld(market_2)

    def test_market_meld_raises_error_when_weighting_is_out_of_range(self):
        market_1 = Market(
            {"alpha_ace": Odds(3), "beta_boy": Odds(3), "delta_dame": Odds(3)}
        )
        market_2 = Market(
            {"alpha_ace": Odds(3), "beta_boy": Odds(3), "delta_dame": Odds(3)}
        )
        with self.assertRaises(ValueError):
            market_1.meld(market_2, 120)

    def test_market_wipe(self):
        self.market.wipe()
        self.assertIsNone(self.market.get("alpha_ace"))

    def test_market_without(self):
        new_market = self.market.without(["beta_boy", "gamma_gal"])
        self.assertEqual(len(new_market), 4)
        self.assertEqual(new_market.percentage, 67)
