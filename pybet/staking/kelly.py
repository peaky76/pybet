from decimal import Decimal

from ..odds import Odds


def kelly(
    true_odds: Odds,
    market_odds: Odds,
    bank: Decimal,
    percentage_commission: Decimal = Decimal("0"),
) -> Decimal:
    """Calculates the stake that should be placed according to the Kelly Criterion
    [https://en.wikipedia.org/wiki/Kelly_criterion], i.e. edge over odds
    for any given true odds at any given market odds for any given bank size

    :param true_odds: The calculated true odds of the selection
    :type true_odds: Odds
    :param market_odds: The odds currently available in the market
    :type market_odds: Odds
    :param bank: The bank available
    :type bank: Decimal
    :param percentage_commission: The percentage commission applied to winnings
    :type percentage_commission: Decimal
    :return: The stake to place according to the Kelly criterion
    :rtype: Decimal


    :Example:
        >>> kelly(Odds(4), Odds(5), 100)
        Decimal('6.25')
        >>> kelly(Odds(5), Odds(4), 100)
        Decimal('0.00')
    """
    if not 0 <= percentage_commission <= 100:
        raise ValueError("Commission must be between 0 and 100")

    p: Decimal = true_odds.to_probability()
    q: Decimal = 1 - p
    odds: Decimal = market_odds.to_one() * Decimal(str(1 - percentage_commission / 100))

    edge: Decimal = (odds * p) - q
    kelly: Decimal = edge / odds

    stake: Decimal = round(bank * max(kelly, Decimal("0")), 2)

    return stake
