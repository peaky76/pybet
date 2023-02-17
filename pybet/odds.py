from __future__ import annotations
from decimal import Decimal
from fractions import Fraction
from typing import overload, List, Tuple, Union


class FractionalOddsSets:

    STANDARD = (
        odds_against := [
            *[f"{x}/1" for x in range(1, 11)],
            *[f"{x}/1" for x in range(12, 23, 2)],
            *[
                f"{x}/1"
                for x in [25, 33, 40, 50, 66, 80, 100, 150, 200, 250, 500, 1000]
            ],
            *[f"{x}/2" for x in range(5, 17, 2)],
            *[f"{x}/4" for x in range(5, 13, 4)],
            *[f"{x}/8" for x in range(11, 17, 2)],
            *["10/3", "6/4", "11/10"],
        ]
    ) + [
        "/".join(x.split("/")[::-1]) for x in odds_against[1:]  # type: ignore
    ]  # [1:] removes 1/1 so it doesn't duplicate


class Odds(Decimal):
    """Allows decimal odds to be created from and converted to
    a range of other odds formats
    """

    # Class methods

    @classmethod
    def evens(cls) -> Odds:
        """Creates Odds instance with value of Evens"""
        return cls(2)

    @overload
    @classmethod
    def fractional(cls, arg: Fraction) -> Odds:
        ...

    @overload
    @classmethod
    def fractional(cls, arg: str) -> Odds:
        ...

    @overload
    @classmethod
    def fractional(cls, arg1: int, arg2: int) -> Odds:
        ...

    @classmethod
    def fractional(cls, *args):
        """Creates Odds instance from fraction-like input,
        including typical odds strings like '9/4', '9-4', '9:4'

        Examples:
            >>> Odds.fractional(Fraction(9, 4))
            3.25
            >>> Odds.fractional('9/4')
            3.25
            >>> Odds.fractional(9, 4)
            3.25
        """

        args = [
            arg if not isinstance(arg, str) else arg.replace("-", "/").replace(":", "/")
            for arg in args
        ]
        fraction = Fraction(*args)

        return cls(fraction.numerator / fraction.denominator + 1)

    @classmethod
    def inverted(cls, value: Decimal) -> Odds:
        """Creates Odds instance that is the inverse of the input value,
        i.e. turns an odds on value into odds against and vice versa

        Example:
            >>> Odds.inverted(5)
            1.25
        """
        return cls(1 / (value - 1) + 1)

    @classmethod
    def moneyline(cls, value: Union[str, int]) -> Odds:
        """Creates Odds instance from American moneyline value

        Example:
            >>> Odds.moneyline(100)
            2
            >>> Odds.moneyline('-150')
            1.67
        """

        value = int(value)
        if abs(value) < 100:
            raise ValueError("Moneyline must be > 100 or < -100")

        return cls(value / 100 + 1) if value > 0 else cls(100 / abs(value) + 1)

    @classmethod
    def percentage(cls, value: Decimal) -> Odds:
        """Creates Odds instance from an equivalent percentage chance > 0 and < 100

        Example:
            >>> Odds.percentage(40)
            2.5
        """

        if not 0 < value < 100:
            raise ValueError("Percentage must be between 0 and 100")

        return cls(100 / value)

    @classmethod
    def probability(cls, value: Decimal) -> Odds:
        """Creates Odds instance from an equivalent probability > 0 and < 1

        Example:
            >>> Odds.probability(0.4)
            2.5
        """

        if not 0 < value < 1:
            raise ValueError("Probability must be between 0 and 1")

        return cls(1 / value)

    # Dunder methods

    def __str__(self) -> str:
        return f"{self:.2f}"

    def __add__(self, other) -> Odds:
        return Odds.percentage(self.to_percentage() + other.to_percentage())

    def __mul__(self, other) -> Odds:
        value = Decimal(self) * Decimal(other)
        return Odds(str(value))

    def __rmul__(self, other) -> Odds:
        return self.__mul__(other)

    def __truediv__(self, other) -> Odds:
        value = (self - 1) / other + 1
        return Odds(str(value))

    # Properties

    @property
    def is_odds_against(self) -> bool:
        """Returns true for odds greater than evens, false otherwise"""
        return self > 2

    @property
    def is_odds_on(self) -> bool:
        """Returns true for odds less than evens, false otherwise"""
        return self < 2

    # Instance methods
    @overload
    def to_fractional(self, fractional_set: List[str], delim: str) -> str:
        ...

    @overload
    def to_fractional(self, fractional_set: List[Fraction], delim: str) -> str:
        ...

    @overload
    def to_fractional(self, fractional_set: List[Tuple[int, int]], delim: str) -> str:
        ...

    def to_fractional(self, fractional_set=FractionalOddsSets.STANDARD, delim="/"):
        """Returns Odds instance as a fractional string with the given delimiter (default '/').
        The return value will be the closest equivalent value found in the given fractional_set.

        Example:
            >>> odds_set = ['3/1', '10/3', '7/2']
            >>> Odds(4.27).to_fractional(odds_set)
            '10/3'
            >>> odds_set = ['3/1', '13/4', '10/3', '7/2']
            >>> Odds(4.27).to_fractional(odds_set, '-')
            '13-4'
        """

        if len(fractional_set) == 0:
            raise ValueError("Fractional odds set contains no odds")

        fractional = Fraction(
            min(fractional_set, key=lambda x: abs(self - Odds.fractional(x)))
        )

        return f"{fractional.numerator}{delim}{fractional.denominator}"

    def to_moneyline(self) -> str:
        """Returns Odds instance as a string moneyline value"""
        if self.is_odds_against:
            return f"+{int(self.to_one() * 100)}"
        return f"-{int(100 / self.to_one())}"

    def to_one(self) -> Decimal:
        """Returns Odds instance as a value "to one", i.e. like fractional odds,
        but the numerator can be a decimal

        Example:
            >>> Odds(5).to_one()
            4
        """
        return self - 1

    def to_percentage(self) -> Decimal:
        """Returns Odds instance as an equivalent percentage chance

        Example:
            >>> Odds(2).to_percentage()
            50
        """
        return 100 / self

    def to_probability(self) -> Decimal:
        """Returns Odds instance as an equivalent probability

        Example:
            >>> Odds(5).to_probability()
            0.2
        """
        return 1 / self

    def shorten(self, percentage_points: Decimal) -> Decimal:
        """Decreases the chance represented by the current Odds instance
        by the specified number of percentage points and returns a new
        Odds instance with that value, i.e. "shortening" the odds

        Example:
            >>> Odds(5).shorten(5)
            4
        """
        return Odds.percentage(self.to_percentage() + percentage_points)

    def lengthen(self, percentage_points: Decimal) -> Decimal:
        """Decreases the chance represented by the current Odds instance
        by the specified number of percentage points and returns a new
        Odds instance with that value, i.e. "lengthening" the odds

        Example:
            >>> Odds(4).lengthen(5)
            5
        """
        return Odds.percentage(self.to_percentage() - percentage_points)
