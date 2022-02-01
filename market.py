"""Module for the Market class"""

from __future__ import annotations
from decimal import Decimal
from typing import Any, List
from odds import Odds


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
        """Returns true if market as a whole in backer's favour, false otherwise """
        return self.percentage < self._fair_percentage

    @property
    def _fair_percentage(self) -> int:
        """Returns the fair market percentage based on number of winning places"""
        return 100 * self.places

    # Instance methods

    def without(self, runners: List[Any]) -> Market:
        """Returns a new market with the specified runners removed"""
        new_items = {key: value for key, value in self.items() if key not in runners}
        return Market(zip(new_items.keys(), new_items.values()))
