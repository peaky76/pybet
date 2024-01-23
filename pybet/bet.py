from decimal import Decimal
from enum import Enum
from functools import reduce
from operator import mul
from typing import Callable

from .odds import Odds


class Bet:
    """A class to represent a bet.

     Attributes:
        stake: The stake of the bet.
        odds: The odds of the bet.
        win_condition: The callback that will determine whether the bet is currently a winner or a loser.
        end_condition: The callback that will determine whether the bet can be settled.

    Example:
        >>> bradford_city = {'position': 1}
        >>> games_played = 45
        >>> bradford_win_league = lambda: bradford_city['position'] == 1
        >>> season_over = lambda: games_played == 46
        >>> bet = Bet(2.00, Odds(21), bradford_win_league, season_over)
    """

    class Status(Enum):
        """An enum to represent the status of a bet."""

        OPEN = 0
        WON = 1
        LOST = 2
        VOID = 3

        def __str__(self):
            return self.name

    def __init__(
        self,
        stake: int | float | Decimal | str,
        odds: Odds | str,
        win_condition: Callable[..., bool],
        end_condition: Callable[..., bool] = lambda: True,
        *,
        bog: bool = False,
    ) -> None:
        """Initialises a bet with a win condition and an end condition.

        :param stake: The stake of the bet
        :type stake: Decimal
        :param odds: The odds of the bet
        :type odds: Odds
        :param win_condition: A callback that will determine whether the bet is currently a winner or a loser
        :type win_condition: Callable[..., bool]
        :param end_condition: A callback that will determine whether the bet can be settled
        :type end_condition: Callable[..., bool]
        :param bog: Whether the bet is best odds guaranteed
        :type bog: bool
        :return: A bet
        :rtype: Bet

        :Example:
            >>> bet = Bet(2.00, Odds(21), bradford_win_league, season_over)
        """
        if not isinstance(odds, Odds) and odds != "SP":
            raise ValueError("Odds must be an instance of Odds or 'SP'")

        self.stake = Decimal(stake)
        self.odds = odds
        self.win_condition = win_condition
        self.end_condition = end_condition
        self.bog = bog
        self._voided = False

    def settle(self, *, sp: Odds = None, rf: int | Decimal = 0) -> Decimal:
        """Returns the returns of the bet.

        :return: The returns of the bet to 2 decimal places
        :rtype: Decimal
        :raises ValueError: If the bet is still open

        :Example:
            >>> bet = Bet(2.00, Odds(21), bradford_win_league, season_over)
            >>> bet.settle()
            ValueError: Bet is still open
            >>> games_played = 46
            >>> bet.settle()
            42.00
            >>> bradford_city['position'] = 2
            >>> bet.settle()
            0
        """

        if self._voided:
            return self.stake

        if not 0 <= rf < 100:
            raise ValueError("Reduction factor must be >= 0 and < 100")

        if not self.end_condition():
            raise ValueError("Bet is still open")

        if not sp:
            if self.odds == "SP":
                raise ValueError("Starting price not set")
            if self.bog:
                raise ValueError("Cannot calculate best odds without starting price")

        settlement_odds = (
            max([sp, self.odds])
            if self.bog and isinstance(self.odds, Odds)
            else sp or self.odds
        )
        reducer = Decimal(1 - rf / 100)
        returns = self.stake * Odds(settlement_odds.to_one() * reducer + 1)

        return Decimal(round(returns, 2) if self.win_condition() else 0)

    @property
    def status(self) -> Status:
        """Returns the status of the bet.

        :return: The status of the bet
        :rtype: Status

        :Example:
            >>> bet = Bet(2.00, Odds(21), bradford_win_league, season_over)
            >>> bet.status
            <Status.OPEN: 0>
            >>> games_played = 46
            <Status.WON: 1>
            >>> bradford_city['position'] = 2
            <Status.LOST: 2>
        """
        if self._voided:
            return Bet.Status.VOID

        if self.end_condition():
            return Bet.Status.WON if self.win_condition() else Bet.Status.LOST

        return Bet.Status.OPEN

    def void(self) -> None:
        """Voids the bet.

        :return: None
        """
        self._voided = True


class Accumulator(Bet):
    def __init__(
        self,
        stake: int | float | Decimal | str,
        bet_list: list[
            list[Odds | str, Callable[..., bool], Callable[..., bool] | None]
        ],
        *,
        bog: bool = False,
    ) -> None:
        odds = reduce(mul, [bet[0] for bet in bet_list], 1)
        win_condition = lambda: all([bet[1]() for bet in bet_list])
        end_condition = lambda: all(
            [(bet[2] if len(bet) == 3 else lambda: True)() for bet in bet_list]
        )

        super().__init__(stake, odds, win_condition, end_condition, bog=bog)
