# pybet
pybet is a library of betting utilities to assist with calculation of bets, stakes and markets

## Installation

`pip install pybet`

## Usage

This initial release contains an Odds class which enables conversion from and to the following types of odds or odds-equivalent:

* Decimal odds, e.g. 2.5
* Fractional odds, e.g. 6/4
* American moneyline odds, e.g. +150 
* Implied percentage, e.g. 40 
* Implied probability, e.g. 0.4

For a basic guide to odds, please see [https://www.investopedia.com/articles/investing/042115/betting-basics-fractional-decimal-american-moneyline-odds.asp]

Internally, the value of an Odds instance is stored as a Decimal, making decimal odds the effective default. 
Odds can be instantiated directly as decimals or via a class method, specifying the type of odds being instantiated from. 
Any Odds instance can then be output to any type with a to_{type} method, e.g.

```
from pybet import Odds

o = Odds(2.5)
o.to_moneyline()    # +150
o.to_percentage()   # 40

o = Odds.fractional(6, 4)
o.to_probability()  # 0.4
```

The to_fractional() method requires a set of fractional odds to work from. It will then select the closest matching value 
from that set. For convenience, a set of standard odds, representing those most typically found in the UK, has been provided.

```
o.to_fractional('5/4', '6/4', '7/4', '2/1') # 6/4
o.to_fractional(Odds.STANDARD_FRACTIONALS) # 6/4
```

Comparisons can be made between Odds instances. It is possible to check if one Odds instance is shorter (<)
or longer (>) than another, e.g.

```
Odds(2.5) < Odds.fractional(11, 4)        # True
Odds.probability(50) > Odds(3)            # False
```

There are properties to compare Odds instances to evens, and a convenience method for evens itself, e.g.

```
o.is_odds_against   # True
o.is_odds_on        # True
Odds.evens() == 2   # True
```

It is possible to invert odds, to turn odds against into the equivalent odds on value and vice versa, e.g.

```
Odds.inverted(2.5) == Odds.fractional(4, 6)  # True
```

There are also operators to perform calculations with Odds instances, though this is more useful in some cases than others.
For example, it is possible to calculate the combined odds of two 3/1 shots as follows:

```
Odds.fractional(3, 1) + Odds.fractional(3, 1) == Odds.evens  # True
```