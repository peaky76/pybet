from decimal import Decimal
from fractions import Fraction
from src.pybet import Odds
from unittest import TestCase


class TestOdds(TestCase):

    def test_odds_standard_fractionals_contains_odds_on(self):
        self.assertTrue('2/5' in Odds.STANDARD_FRACTIONALS)

    def test_odds_standard_fractionals_contains_odds_against_short(self):
        self.assertTrue('5/2' in Odds.STANDARD_FRACTIONALS)

    def test_odds_standard_fractionals_contains_odds_against_long(self):
        self.assertTrue('66/1' in Odds.STANDARD_FRACTIONALS)

    def test_odds_can_init_with_decimal(self):
        self.assertEqual(3.25, Odds(Decimal('3.25')))

    def test_odds_can_init_with_float(self):
        self.assertEqual(3.25, Odds(3.25))

    def test_odds_can_init_with_int(self):
        self.assertEqual(3, Odds(3))

    def test_odds_evens(self):
        self.assertEqual(2, Odds.evens())

    def test_odds_can_init_with_fractional_ints(self):
        self.assertEqual(3.25, Odds.fractional(9, 4))

    def test_odds_can_init_with_fractional_string(self):
        self.assertEqual(3.25, Odds.fractional('9/4'))

    def test_odds_can_init_with_fractional_colon_string(self):
        self.assertEqual(3.25, Odds.fractional('9:4'))

    def test_odds_can_init_with_fractional_hyphenated_string(self):
        self.assertEqual(3.25, Odds.fractional('9-4'))

    def test_odds_can_init_with_fractional_fraction(self):
        self.assertEqual(3.25, Odds.fractional(Fraction('9/4')))

    def test_odds_can_init_with_inverted_decimal(self):
        self.assertEqual(1.5, Odds.inverted(Decimal('3.0')))

    def test_odds_can_init_with_inverted_float(self):
        self.assertEqual(1.5, Odds.inverted(3.0))

    def test_odds_can_init_with_inverted_int(self):
        self.assertEqual(1.5, Odds.inverted(3))

    def test_odds_can_init_with_inverted_odds(self):
        self.assertEqual(1.5, Odds.inverted(Odds(3)))

    def test_odds_can_init_with_moneyline_positive(self):
        self.assertEqual(2.38, Odds.moneyline(138))

    def test_odds_can_init_with_moneyline_negative(self):
        self.assertAlmostEqual(Decimal(1.67), Odds.moneyline(-150), places=2)

    def test_odds_can_init_with_moneyline_string_positive(self):
        self.assertEqual(2.38, Odds.moneyline('+138'))

    def test_odds_can_init_with_moneyline_string_negative(self):
        self.assertAlmostEqual(Decimal(1.67), Odds.moneyline('-150'), places=2)

    def test_odds_can_init_with_moneyline_evens_positive(self):
        self.assertEqual(2, Odds.moneyline(100))

    def test_odds_can_init_with_moneyline_evens_negative(self):
        self.assertEqual(2, Odds.moneyline(-100))

    def test_odds_cannot_init_with_moneyline_under_100_positive(self):
        self.assertRaises(ValueError, lambda: Odds.moneyline(80))

    def test_odds_cannot_init_with_moneyline_under_100_negative(self):
        self.assertRaises(ValueError, lambda: Odds.moneyline(-80))

    def test_odds_can_init_with_percentage_decimal(self):
        self.assertEqual(2.5, Odds.percentage(Decimal('40')))

    def test_odds_can_init_with_percentage_float(self):
        self.assertEqual(2.5, Odds.percentage(40.0))

    def test_odds_can_init_with_percentage_int(self):
        self.assertEqual(2.5, Odds.percentage(40))

    def test_odds_cannot_init_with_percentage_too_high(self):
        self.assertRaises(ValueError, lambda: Odds.percentage(110))

    def test_odds_cannot_init_with_percentage_too_low(self):
        self.assertRaises(ValueError, lambda: Odds.percentage(-10))

    def test_odds_cannot_init_with_percentage_100(self):
        self.assertRaises(ValueError, lambda: Odds.percentage(100))

    def test_odds_cannot_init_with_percentage_0(self):
        self.assertRaises(ValueError, lambda: Odds.percentage(0))

    def test_odds_can_init_with_probability_decimal(self):
        self.assertEqual(2.5, Odds.probability(Decimal('0.4')))

    def test_odds_can_init_with_probability_float(self):
        self.assertEqual(2.5, Odds.probability(0.4))

    def test_odds_cannot_init_with_probability_too_high(self):
        self.assertRaises(ValueError, lambda: Odds.probability(1.1))

    def test_odds_cannot_init_with_probability_too_low(self):
        self.assertRaises(ValueError, lambda: Odds.probability(-0.1))

    def test_odds_cannot_init_with_probability_1(self):
        self.assertRaises(ValueError, lambda: Odds.probability(1))

    def test_odds_cannot_init_with_probability_0(self):
        self.assertRaises(ValueError, lambda: Odds.probability(0))

    def test_odds_less_than_is_true(self):
        self.assertTrue(Odds.percentage(40) < Odds('3.25'))

    def test_odds_less_than_is_false(self):
        self.assertFalse(Odds.fractional(9, 4) < Odds('3.25'))

    def test_odds_equals_is_true(self):
        self.assertTrue(Odds.fractional(9, 4) == Odds('3.25'))

    def test_odds_equals_is_false(self):
        self.assertFalse(Odds.percentage(40) == Odds.fractional(9, 4))

    def test_odds_greater_than_is_true(self):
        self.assertTrue(Odds.fractional(9, 4) > Odds.percentage(40))

    def test_odds_greater_than_is_false(self):
        self.assertFalse(Odds.fractional(9, 4) > Odds('3.25'))

    def test_odds_add(self):
        self.assertAlmostEqual(Decimal(70.77), (Odds.percentage(40) + Odds.fractional(9, 4)).to_percentage(), places=2)

    def test_odds_lmul_with_odds(self):
        self.assertEqual(8.125, Odds('3.25') * Odds.percentage(40))

    def test_odds_lmul_with_decimal(self):
        self.assertEqual(8.125, Odds('3.25') * Decimal(2.5))

    def test_odds_rmul_with_odds(self):
        self.assertEqual(8.125, Odds.percentage(40) * Odds('3.25'))

    def test_odds_rmul_with_decimal(self):
        self.assertEqual(8.125, Decimal(2.5) * Odds('3.25'))

    def test_odds_truediv(self):
        self.assertEqual(Decimal('1.45'), Odds('3.25') / 5)

    def test_odds_remain_odds_after_mul_with_odds(self):
        self.assertAlmostEqual(Decimal(12.31), (Odds.percentage(40) * Odds('3.25')).to_percentage(), places=2)

    def test_odds_remain_odds_after_mul_with_decimal(self):
        self.assertAlmostEqual(Decimal(12.31), (Decimal(2.5) * Odds('3.25')).to_percentage(), places=2)

    def test_odds_is_odds_against_is_true(self):
        self.assertTrue(Odds.percentage(40).is_odds_against)

    def test_odds_is_odds_against_is_false(self):
        self.assertFalse(Odds.inverted(3).is_odds_against)

    def test_odds_is_odds_against_is_false_for_evens(self):
        self.assertFalse(Odds.evens().is_odds_against)

    def test_odds_is_odds_on_is_true(self):
        self.assertTrue(Odds.inverted(3).is_odds_on)

    def test_odds_is_odds_on_is_false(self):
        self.assertFalse(Odds.percentage(40).is_odds_on)

    def test_odds_is_odds_on_is_false_for_evens(self):
        self.assertFalse(Odds.evens().is_odds_on)

    def test_odds_to_decimal(self):
        self.assertEqual(2.5, Odds.percentage(40))

    def test_odds_to_fractional_exact(self):
        odds_set = ['3/1', '10/3', '7/2', '4/1']
        odds = Odds(5)
        self.assertEqual('4/1', odds.to_fractional(odds_set))

    def test_odds_to_fractional_closest_above(self):
        odds_set = ['3/1', '10/3', '7/2', '4/1']
        odds = Odds(4.27)
        self.assertEqual('10/3', odds.to_fractional(odds_set))

    def test_odds_to_fractional_closest_below(self):
        odds_set = ['3/1', '13/4', '10/3', '7/2', '4/1']
        odds = Odds(4.27)
        self.assertEqual('13/4', odds.to_fractional(odds_set))

    def test_odds_to_fractional_with_different_delimiter(self):
        odds_set = ['3/1', '13/4', '10/3', '7/2', '4/1']
        odds = Odds(4.27)
        self.assertEqual('13:4', odds.to_fractional(odds_set, ':'))

    def test_odds_to_fractional_with_standard_fractionals_constants(self):
        odds_set = Odds.STANDARD_FRACTIONALS
        odds = Odds(5)
        self.assertEqual('4/1', odds.to_fractional(odds_set))

    def test_odds_to_fractional_uses_standard_fractionals_as_default_if_not_specified(self):
        odds = Odds(5)
        self.assertEqual('4/1', odds.to_fractional())

    def test_odds_to_fractional_raises_error_with_no_fractional_set(self):
        self.assertRaises(ValueError, lambda: Odds('4.30').to_fractional([]))

    def test_odds_to_fractional_raises_error_with_incorrect_fractional_set(self):
        self.assertRaises(TypeError, lambda: Odds('4.30').to_fractional([(2), (4, 1), (6, 3, 1)]))

    def test_odds_to_moneyline_positive(self):
        self.assertEqual('+225', Odds.fractional(9, 4).to_moneyline())

    def test_odds_to_moneyline_negative(self):
        self.assertEqual('-200', Odds.inverted(3).to_moneyline())

    def test_odds_to_one_decimal(self):
        self.assertEqual(2.25, Odds('3.25').to_one())

    def test_odds_to_one_int(self):
        self.assertEqual(2, Odds(3).to_one())

    def test_odds_to_percentage(self):
        self.assertAlmostEqual(Decimal('30.7692'), Odds.fractional(9, 4).to_percentage(), places=4)

    def test_odds_to_probability(self):
        self.assertAlmostEqual(Decimal('0.3077'), Odds.fractional(9, 4).to_probability(), places=4)

    def test_odds_shorten(self):
        self.assertEqual(2, Odds.percentage(40).shorten(10))

    def test_odds_lengthen(self):
        self.assertAlmostEqual(Decimal('3.3333'), Odds.percentage(40).lengthen(10), places=4)
