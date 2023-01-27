"""Kelly Criterion method"""

from __future__ import annotations
from decimal import Decimal
from ..odds import Odds


def kelly(true_odds: Odds, market_odds: Odds, bank: Decimal) -> Decimal:
    """Calculates the stake that should be placed according to the Kelly Criterion
    [https://en.wikipedia.org/wiki/Kelly_criterion], i.e. edge over odds
    for any given true odds at any given market odds for any given bank size

    Example:
        >>> kelly(Odds(4), Odds(5), bank: 100) # Odds in bettor's favour
        6.25
        >>> kelly(Odds(5), Odds(4), bank: 100) # Odds in bookmaker's favour
        0.00
    """

    p = true_odds.to_probability()
    q = 1 - p
    b = market_odds.to_one()

    kelly_percentage = (b * p - q) / b
    stake = bank * kelly_percentage if kelly_percentage > 0.0 else 0

    return stake
