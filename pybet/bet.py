from decimal import Decimal
from enum import Enum
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
        >>> dice_rolled = False
        >>> def dice_roll():
        >>>     return rand.randint(1, 6)
        >>> bet = Bet(lambda: dice_roll() == 6, dice_rolled)
    """

    class Status(Enum):
        """An enum to represent the status of a bet."""

        OPEN = 0
        WON = 1
        LOST = 2

        def __str__(self):
            return self.name

    def __init__(
        self,
        stake: Decimal,
        odds: Odds,
        win_condition: Callable[..., bool],
        end_condition: Callable[..., bool],
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
        :return: A bet
        :rtype: Bet

        :Example:
            >>> bet = Bet(lambda: dice_roll() == 6, dice_rolled)
        """
        self.stake = stake
        self.odds = odds
        self.win_condition = win_condition
        self.end_condition = end_condition

    @property
    def is_settled(self):
        """Returns whether the bet is settled.

        :return: Whether the bet is settled
        :rtype: bool

        :Example:
            >>> dice_rolled = False
            >>> bet = Bet(lambda: dice_roll() == 6, dice_rolled)
            >>> bet.is_settled
            False
            >>> dice_rolled = True
            >>> bet.is_settled
            True
        """
        return self.end_condition()

    @property
    def status(self):
        """Returns the status of the bet.

        :return: The status of the bet
        :rtype: Status

        :Example:
            >>> dice_rolled = False
            >>> bet = Bet(lambda: dice_roll() == 6, dice_rolled)
            >>> bet.status
            Status.OPEN
            >>> dice_rolled = True
            >>> bet.status
            Status.WON
        """
        if self.is_settled:
            return Bet.Status.WON if self.win_condition() else Bet.Status.LOST

        return Bet.Status.OPEN
