from __future__ import annotations
from decimal import Decimal
from functools import reduce
from itertools import permutations
from operator import mul
from typing import Any, List
from .odds import Odds


class Market(dict):
    """A betting market represented by a dictionary of runners and odds

    Attributes:
        places: The number of winning places in the market (default 1, i.e. win only).

    Example:
        >>> runners = ['Frankel', 'Sea The Stars', 'Nijinsky', 'Mill Reef', 'Quixall Crossett']
        >>> odds = [Odds(x) for x in [2, 4, 5, 10, 1000]]
        >>> market = Market(zip(runners, odds), places=2)
    """

    places: int = 1

    def __setitem__(self, key: Any, value: Any):
        if not isinstance(value, Odds) and value is not None:
            value = Odds(value)
        super().__setitem__(key, value)

    # Properties

    @property
    def percentage(self) -> Decimal:
        """The total market percentage of all runners

        :return: The percentage market
        :rtype: Decimal
        """

        return sum([odds.to_percentage() for odds in self.values()])

    @property
    def overround_per_runner(self) -> Decimal:
        """Excess market percentage divided by number of runners

        :return: The overround per runner
        :rtype: Decimal
        """

        return (self.percentage - self._fair_percentage) / len(self)

    @property
    def favourites(self) -> List[Any]:
        """Returns list of runners that are favourite for the event
        Note: Will be a list even if there is only one favourite

        :return: A list of market favourites
        :rtype: List[Any]
        """

        return [runner for runner, odds in self.items() if odds == min(self.values())]

    @property
    def is_overround(self) -> bool:
        """Whether the market is overround or not

        :return: True if market as a whole in layer's favour, false otherwise
        :rtype: bool
        """

        return self.percentage > self._fair_percentage

    @property
    def is_fair(self) -> bool:
        """Whether the market has no bias in favour of backer or layer

        :return: True if there is no inbuilt margin, false otherwise
        :rtype: bool
        """

        return self.percentage == self._fair_percentage

    @property
    def is_overbroke(self) -> bool:
        """Whether the market has no bias in favour of bettor or layer

        :return: True if market as a whole in backer's favour, false otherwise
        :rtype: bool
        """

        return self.percentage < self._fair_percentage

    @property
    def _fair_percentage(self) -> int:
        """What a fair percentage would be for the market based on the number of winning places

        :return: The fair market percentage based on number of winning places
        :rtype: int
        """

        return 100 * self.places

    # Instance methods

    def apply_margin(self, margin: Decimal) -> Market:
        """Applies the specified margin to each runner's underlying price, and thus to the overround. It is not applied cumulatively,
        i.e. a 10% margin applied to a market with a 105% overround, will become a 110% market, not 115%.

        :param margin: The margin to apply to the market
        :type margin: Decimal
        :return: A revised market with the specified margin built in
        :rtype: Market

        :Example:
            >>> market = Market({'Frankel': Odds(3), 'Sea The Stars': Odds(3), 'Nijinsky': Odds(3)})
            >>> market.apply_margin(20).get('Frankel')
            Decimal('2.5')
        """

        adjustment = (100 + margin) / self.percentage
        for runner, odds in self.items():
            self[runner] = Odds(Decimal(odds) / adjustment)
        return self

    def derive(self, places: int, *, discounts: List[float] | None = None) -> Market:
        """Derives a place market from a win market using the Harville formula (see https://en.wikipedia.org/wiki/Harville_formula)
        applying a specified discounted version of that formula if required

        :param places: The number of places to derive the market for
        :type places: int
        :param discounts: A list of discounts to apply to the probability of each horse in the market, defaults to None
        :type discounts: List[float], optional
        :raises ValueError: If the number of places is invalid
        :raises ValueError: If the market is not a win market
        :return: A revised market with the specified number of places
        :rtype: Market

        :Example:
            >>> market = Market({'Frankel': Odds(3), 'Sea The Stars': Odds(3), 'Nijinsky': Odds(3)})
            >>> market.derive(2).get('Frankel')
            Decimal('1.5')
        """

        if self.places != 1:
            raise ValueError("Derivation only possible from win market")

        if places >= len(self) or places <= 1:
            raise ValueError("Invalid number of places")

        fair_market = Market(self)
        fair_market.apply_margin(Decimal("0"))
        derived_market = Market.fromkeys(self.keys())
        prob = lambda x: float(fair_market[x].to_probability())
        product = lambda x: reduce(mul, x, 1)
        prob_exponent = lambda x, y: prob(x) ** discounts[y] if discounts else prob(x)

        for perm in list(permutations(self.keys(), places)):
            denominator = product([prob_exponent(h, i) for i, h in enumerate(perm)])
            numerator = product(
                [
                    sum(prob_exponent(h, i) for h in self.keys() if h not in perm[:i])
                    for i, _ in enumerate(perm)
                ]
            )
            perm_probability = Decimal(denominator / numerator)

            for horse in perm:
                derived_market[horse] = (derived_market[horse] or 0) + Odds.probability(
                    perm_probability
                )

        place_market = Market(derived_market)
        place_market.places = places

        return place_market

    def equalise(self) -> Market:
        """Resets a market so that all runners have equal odds with no overround

        :return: A revised market with no margin built in
        :rtype: Market

        :Example:
            >>> market = Market({'Frankel': Odds(2.5), 'Sea The Stars': Odds(2.5), 'Nijinsky': Odds(2.5), 'Dancing Brave': Odds(2.5)})
            >>> market.equalise().get('Frankel')
            Decimal('4')
        """
        self.wipe()
        self.fill()
        return self

    def fill(self, margin: Decimal = Decimal(0)) -> Market:
        """Fills out any missing odds in the market proportionately so that the specified margin is achieved

        :param margin: The margin to build into the market, defaults to zero
        :type margin: Decimal, optional
        :raises ValueError: if there is already a larger margin built into the market
        :return: A market with all missing odds filled in
        :rtype: Market

        :Example:
            >>> market = Market({'Frankel': Odds(4), 'Sea The Stars': Odds(4), 'Nijinsky': Odds(4), 'Dancing Brave': None})
            >>> market.fill().get('Dancing Brave')
            Decimal('4')
        """
        unpriced_runners = [
            runner for runner in self.keys() if self.get(runner) is None
        ]
        missing_percentage = (100 + margin) - self.without(unpriced_runners).percentage

        if missing_percentage <= 0:
            raise ValueError("Market already equals or exceeds specified margin")

        odds_to_apply = Odds.percentage(missing_percentage / len(unpriced_runners))
        for runner in unpriced_runners:
            self[runner] = odds_to_apply

        return self

    def meld(self, other: Market, other_percentage: float = 50) -> Market:
        """Melds two markets together so that the odds for each runner are a weighted average of the two markets

        :param other: The market to meld with
        :type other: Market
        :param other_percentage: The percentage of the melded market that should be made up of the other market, defaults to 50
        :type other_percentage: float, optional
        :raises ValueError: if the two markets do not have the same runners
        :return: A market with the weighted average odds of the two markets
        """

        if self.keys() != other.keys():
            raise ValueError("Markets must have the same runners")

        if not 0 <= other_percentage <= 100:
            raise ValueError("Percentage must be between 0 and 100")

        new_market = Market(zip(self.keys(), [None] * len(self)))
        market_1 = self.apply_margin(Decimal(0))
        market_2 = other.apply_margin(Decimal(0))
        for runner in self.keys():
            new_market[runner] = Odds.percentage(
                (market_1[runner].to_percentage() * (100 - other_percentage) / 100)
                + (market_2[runner].to_percentage() * other_percentage / 100)
            )

        return new_market

    def wipe(self) -> Market:
        """Wipe market so that none of the runners have any odds

        :return: An empty market
        :rtype: Market

        :Example:
            >>> market = Market({'Frankel': Odds(4), 'Sea The Stars': Odds(4), 'Nijinsky': Odds(4), 'Dancing Brave': Odds(4)})
            >>> list(market.wipe().values())
            [None, None, None, None]
        """

        for runner in self.keys():
            self[runner] = None
        return self

    def without(self, runners: List[Any]) -> Market:
        """Create a new market with the specified runners removed

        :param runners: Runners to remove from the market
        :type runners: List[Any]
        :return: A new market without the specified runners
        :rtype: Market

        :Example:
            >>> market = Market({'Frankel': Odds(4), 'Sea The Stars': Odds(4), 'Nijinsky': Odds(4), 'Dancing Brave': Odds(4)})
            >>> new_market = market.without(['Frankel'])
            >>> list(new_market.keys())
            ['Sea The Stars', 'Nijinsky', 'Dancing Brave']
        """

        return Market({key: value for key, value in self.items() if key not in runners})
