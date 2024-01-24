from peak_utility.number import Numbertext

from .bet import Accumulator, Bet, Double, Treble

__all__ = ["Accumulator", "Bet", "Double", "Treble"]

for i in range(4, 21):
    name = f"{Numbertext(i).__str__().title()}Fold"
    globals()[name] = type(name, (Accumulator,), {"_selection_count_requirement": i})
    __all__ += name
