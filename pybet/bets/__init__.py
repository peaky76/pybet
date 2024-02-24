from peak_utility.number import Numbertext # type: ignore

from .accumulator import Accumulator
from .bet import Bet
from .double import Double
from .treble import Treble

__all__ = ["Accumulator", "Bet", "Double", "Treble"]

for i in range(4, 21):
    name = f"{Numbertext(i).__str__().title()}Fold"
    globals()[name] = type(name, (Accumulator,), {"_selection_count_requirement": i})
    __all__ += name
