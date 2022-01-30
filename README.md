# pybet
pybet is a library of betting utilities to assist with calculation of bets, stakes and markets

## Installation

`pip install pybet`

## Usage

This initial release contains an Odds class which enables conversion from and to the following types of odds or odds-equivalent:

* Decimal odds, e.g. 2.5
* Fractional odds, e.g. 6/4
* American moneyline odds, e.g. +150 
* Percentage, e.g. 40 
* Probability, e.g. 0.4

Odds are stored internally as decimals. They can be instantiated directly as decimals or via a class method, specifying
the type of odds being instantiated from. Any Odds instance can then be output to any type with a to_{type} method, e.g.

`
from pybet import Odds

o = Odds(2.5)
o.to_moneyline()

>> +150

o.to_percentage()

>> 40

o.to_probability()

>> 0.4
`

The to_fractional() method requires a set of fractional odds to work from. It will then select the item from the set of odds
that most closely matches.

`
o.to_fractional('5/4', '6/4', '7/4', '2/1')

>> 6/4
`