from __future__ import annotations
from decimal import Decimal
from fractions import Fraction
from typing import overload, List, Tuple, Union


class FractionalOddsSets:
    """Constant lists of fractional odds for use in Odds instances to determine the proximate fractional odds to any particular value"""

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
    """A class that allows decimal odds to be created from and converted to a range of other odds formats"""

    # Class methods

    @classmethod
    def evens(cls) -> Odds:
        """Convenience constructor for creating an Odds value of evens

        :return: An Odds instance equal to evens
        :rtype: Odds
        """

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

    @classmethod  # type: ignore
    def fractional(cls, *args) -> Odds:
        """Creates an Odds instance from fraction-like input, including typical odds strings like '9/4', '9-4', '9:4'

        :return: An Odds instance equal to the value of the fraction passed in
        :rtype: Odds

        :Example:
            >>> Odds.fractional(Fraction(9, 4))
            Decimal('3.25')
            >>> Odds.fractional('9/4')
            Decimal('3.25')
            >>> Odds.fractional(9, 4)
            Decimal('3.25')
        """

        args = [  # type: ignore
            arg if not isinstance(arg, str) else arg.replace("-", "/").replace(":", "/")
            for arg in args
        ]
        fraction = Fraction(*args)

        return cls(fraction.numerator / fraction.denominator + 1)

    @classmethod
    def inverted(cls, value: Decimal) -> Odds:
        """Creates an Odds instance that is the inverse of the input value, i.e. turns an odds on value into odds against and vice versa

        :param value: A decimal representation of the odds to invert
        :type value: Decimal
        :return: An odds instance representing the inverse of the value passed in
        :rtype: Odds

        :Example:
            >>> Odds.inverted(5)
            Decimal('1.25')
        """

        return cls(1 / (value - 1) + 1)

    @classmethod
    def moneyline(cls, value: Union[str, int]) -> Odds:
        """Creates an Odds instance from an American moneyline value

        :param value: A representation of the moneyline value, e.g. -90
        :type value: Union[str, int]
        :raises ValueError: if the value is between the bounds of -100 and 100 and not suitable for moneyline values
        :return: An odds instance representing the moneyline value passed in
        :rtype: Odds

        :Example:
            >>> Odds.moneyline(100)
            Decimal('2.0')
            >>> Odds.moneyline('-125')
            Decimal('1.8')
        """

        value = int(value)
        if abs(value) < 100:
            raise ValueError("Moneyline must be > 100 or < -100")

        return (
            cls(Decimal(str(value / 100)) + 1)
            if value > 0
            else cls(Decimal(str(100 / abs(value))) + 1)
        )

    @classmethod
    def percentage(cls, value: Decimal) -> Odds:
        """Creates an Odds instance from an equivalent percentage chance > 0 and < 100


        :param value: A representation of the odds as a percentage
        :type value: Decimal
        :raises ValueError: if the value is not between 0 and 100%
        :return: An odds instance representing the percentage value passed in
        :rtype: Odds

        :Example:
            >>> Odds.percentage(40)
            Decimal('2.5')
        """

        if not 0 < value < 100:
            raise ValueError("Percentage must be between 0 and 100")

        return cls(100 / value)

    @classmethod
    def probability(cls, value: Decimal) -> Odds:
        """Creates an Odds instance from an equivalent probability > 0 and < 1

        :param value: A representation of the odds as a probability
        :type value: Decimal
        :raises ValueError: if the value is not between 0 and 1
        :return: An odds instance representing the probability passed in
        :rtype: Odds

        :Example:
            >>> Odds.probability(0.4)
            Decimal('2.5')
        """

        if not 0 < value < 1:
            raise ValueError("Probability must be between 0 and 1")

        return cls(1 / value)

    # Dunder methods

    def __str__(self) -> str:
        """A string representation of the odds as a decimal to two decimal places

        :return: The odds to two decimal places
        :rtype: str

        :Example:
            >>> str(Odds(3.25))
            '3.25'
        """

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
        """Whether the Odds instance is odds against

        :return: True for odds greater than evens, false otherwise
        :rtype: bool

        :Example:
            >>> Odds(3).is_odds_against
            True
            >>> Odds(0.33).is_odds_against
            False
        """

        return self > 2

    @property
    def is_odds_on(self) -> bool:
        """Whether the Odds instance is odds against

        :return: True for odds less than evens, false otherwise
        :rtype: bool

        :Example:
            >>> Odds(0.33).is_odds_on
            True
            >>> Odds(3).is_odds_on
            False
        """

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

    def to_fractional(  # type: ignore
        self,
        fractional_set=FractionalOddsSets.STANDARD,
        delim="/",
    ) -> str:
        """Returns an Odds instance as a fractional string with the given delimiter (default '/').
        The return value will be the closest equivalent value found in the given fractional_set.

        :param fractional_set: A set of fractional odds to select from, defaults to standard UK fractionals
        :type fractional_set: List[str], optional
        :param delim: A delimiter for the odds string, defaults to "/"
        :type delim: str, optional
        :raises ValueError: if the odds set provided is empty
        :return: A string representation of the odds in fractional form
        :rtype: str

        :Example:
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
        """Returns an Odds instance as a string moneyline value

        :return: An Odds instance in moneyline format
        :rtype: str

        :Example:
            >>> Odds.evens().to_moneyline()
            '-100'
        """

        if self.is_odds_against:
            return f"+{int(self.to_one() * 100)}"
        return f"-{int(100 / self.to_one())}"

    def to_one(self) -> Decimal:
        """Returns Odds instance as a value "to one", i.e. like fractional odds, but the numerator can be a decimal

        :return: The Odds instance adjusted to a "to one" value
        :rtype: Decimal

        :Example:
            >>> Odds(5).to_one()
            Decimal('4')
        """

        return self - 1

    def to_percentage(self) -> Decimal:
        """Returns an Odds instance as an equivalent percentage chance

        :return: The Odds instance as a percentage
        :rtype: Decimal

        :Example:
            >>> Odds(5).to_percentage()
            Decimal('20')
        """

        return 100 / self

    def to_probability(self) -> Decimal:
        """Returns an Odds instance as an equivalent probability

        :return: The Odds instance as a probability
        :rtype: Decimal

        :Example:
            >>> Odds(5).to_probability()
            Decimal('0.2')
        """

        return 1 / self

    def shorten(self, percentage_points: Decimal) -> Odds:
        """Decreases the chance represented by the current Odds instance by the specified number of
        percentage points and returns a new Odds instance with that value, i.e. "shortening" the odds

        :param percentage_points: Number of percentage points by which to decrease the chance represented by the Odds
        :type percentage_points: Decimal
        :return: A new Odds instance
        :rtype: Decimal

        :Example:
            >>> Odds(5).shorten(5)
            Decimal('4')
        """

        return Odds.percentage(self.to_percentage() + percentage_points)

    def lengthen(self, percentage_points: Decimal) -> Decimal:
        """Increases the chance represented by the current Odds instance by the specified number of
        percentage points and returns a new Odds instance with that value, i.e. "lengthening" the odds

        :param percentage_points: Number of percentage points by which to increase the chance represented by the Odds
        :type percentage_points: Decimal
        :return: A new Odds instance
        :rtype: Decimal

        :Example:
            >>> Odds(4).lengthen(5)
            Decimal('5')
        """

        return Odds.percentage(self.to_percentage() - percentage_points)
