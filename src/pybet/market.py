"""Module for the Market class"""

from __future__ import annotations
from decimal import Decimal
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
        """Returns total market percentage of all runners"""
        return sum([odds.to_percentage() for odds in self.values()])

    @property
    def overround_per_runner(self) -> Decimal:
        """Returns excess market percentage divided by number of runners"""
        return (self.percentage - self._fair_percentage) / len(self)

    @property
    def favourites(self) -> List[Any]:
        """Returns list of runners that are favourite for the event
        Note: Will be a list even if there is only one favourite
        """
        return [runner for runner, odds in self.items() if odds == min(self.values())]

    @property
    def is_overround(self) -> bool:
        """Returns true if market as a whole in layer's favour, false otherwise"""
        return self.percentage > self._fair_percentage

    @property
    def is_fair(self) -> bool:
        """Returns true if there is no inbuilt margin"""
        return self.percentage == self._fair_percentage

    @property
    def is_overbroke(self) -> bool:
        """Returns true if market as a whole in backer's favour, false otherwise"""
        return self.percentage < self._fair_percentage

    @property
    def _fair_percentage(self) -> int:
        """Returns the fair market percentage based on number of winning places"""
        return 100 * self.places

    # Instance methods

    def apply_margin(self, margin: Decimal) -> Market:
        """Returns a revised market with the specified margin built in to each runner's price,
        and thus to the overround. It is not applied cumulatively, i.e. a 10% margin applied
        to a market with a 105% overround, will become a 110% market, not 115%.  

        Example:
            >>> market = Market({'Frankel': 3, 'Sea The Stars': 3, 'Nijinsky': 3})
            >>> market.apply_margin(20)
            >>> market.get('Frankel')
            2.5
        """
        adjustment = (100 + margin) / self.percentage
        for runner, odds in self.items():
            self[runner] = Odds(Decimal(odds) / adjustment)
        return self

    def clear(self):
        """Nulls all odds, restoring an empty market"""
        for runner in self.keys():
            self[runner] = None
        return self

    def fill(self, margin: Decimal = 0) -> Market:
        """Fills out null odds in the market proportionately so that the specified
        margin is achieved
        """
        unpriced_runners = [runner for runner in self.keys() if self.get(runner) is None]
        missing_percentage = (100 + margin) - self.without(unpriced_runners).percentage

        if missing_percentage <= 0:
            raise ValueError('Market already equals or exceeds specified margin')

        odds_to_apply = Odds.percentage(missing_percentage / len(unpriced_runners))
        for runner in unpriced_runners:
            self[runner] = odds_to_apply

        return self

    def share_for(self, runner: Any) -> Decimal:
        """Returns the market share for the specified runner, i.e. the percentage of the
        theoretical market which is attributable to that runner
        """
        return (self[runner].to_percentage() / self.percentage) * 100

    def without(self, runners: List[Any]) -> Market:
        """Returns a new market with the specified runners removed"""
        return Market({key: value for key, value in self.items() if key not in runners})
