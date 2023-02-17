from __future__ import annotations
from decimal import Decimal
from ..odds import Odds


def kelly(true_odds: Odds, market_odds: Odds, bank: Decimal) -> Decimal:
    """Calculates the stake that should be placed according to the Kelly Criterion
    [https://en.wikipedia.org/wiki/Kelly_criterion], i.e. edge over odds
    for any given true odds at any given market odds for any given bank size

    :param true_odds: The calculated true odds of the selection
    :type true_odds: Odds
    :param market_odds: The odds currently available in the market
    :type market_odds: Odds
    :param bank: The bank available
    :type bank: Decimal
    :return: The stake to place according to the Kelly criterion
    :rtype: Decimal


    :Example:
        >>> kelly(Odds(4), Odds(5), 100)
        Decimal('6.25')
        >>> kelly(Odds(5), Odds(4), 100)
        Decimal('0.00')
    """

    p = true_odds.to_probability()
    q = 1 - p
    b = market_odds.to_one()

    kelly_percentage = (b * p - q) / b
    stake = round(
        (Decimal(bank * kelly_percentage) if kelly_percentage > 0.0 else Decimal(0.00)),
        2,
    )

    return stake
