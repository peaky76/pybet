from typing import Callable


class Bet:
    """A class to represent a bet.

     Attributes:
        win_condition: The callback that will determine whether the bet is currently a winner or a loser.
        end_condition: The callback that will determine whether the bet can be settled.

    Example:
        >>> dice_rolled = False
        >>> def dice_roll():
        >>>     return rand.randint(1, 6)
        >>> bet = Bet(lambda: dice_roll() == 6, dice_rolled)
    """

    def __init__(
        self, win_condition: Callable[..., bool], end_condition: Callable[..., bool]
    ) -> None:
        """Initialises a bet with a win condition and an end condition.

        :param win_condition: A callback that will determine whether the bet is currently a winner or a loser
        :type win_condition: Callable[..., bool]
        :param end_condition: A callback that will determine whether the bet can be settled
        :type end_condition: Callable[..., bool]
        :return: A bet
        :rtype: Bet

        :Example:
            >>> bet = Bet(lambda: dice_roll() == 6, dice_rolled)
        """
        self.win_condition = win_condition
        self.end_condition = end_condition
