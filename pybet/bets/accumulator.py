from decimal import Decimal
from functools import reduce
from operator import mul
from typing import Callable

from pybet import Odds

from .bet import Bet


class Accumulator(Bet):
    _selection_count_requirement: int | None = None

    def __new__(
        cls,
        stake: float | Decimal | str,
        bet_list: list[
            tuple[Odds | str, Callable[..., bool], Callable[..., bool] | None]
        ],
        *,
        bog: bool = False,
    ):
        if (
            cls._selection_count_requirement
            and len(bet_list) != cls._selection_count_requirement
        ):
            raise ValueError(
                f"{cls.__name__} must have {cls._selection_count_requirement} selections"
            )

        return super().__new__(cls)

    def __init__(
        self,
        stake: float | Decimal | str,
        bet_list: list[
            tuple[Odds | str, Callable[..., bool], Callable[..., bool] | None]
        ],
        *,
        bog: bool = False,
    ) -> None:
        odds = reduce(mul, [Odds(bet[0]) for bet in bet_list], 1)
        win_condition = lambda: all(bet[1]() for bet in bet_list)
        end_condition = lambda: all(
            bet[2]() if len(bet) == 3 and bet[2] else True for bet in bet_list
        )

        super().__init__(stake, Odds(odds), win_condition, end_condition, bog=bog)
