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

and a Market class which allows for the creation of markets based on those odds and some limited calculations on those markets

For a basic guide to odds, please see [https://www.investopedia.com/articles/investing/042115/betting-basics-fractional-decimal-american-moneyline-odds.asp]

### Odds

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

It is also possible to get the odds "to one" i.e. the numerator of fractional odds, but with a decimal numerator if that is applicable, 
or, put another way, the fractional odds with the stake removed.

```
Odds.fractional(5, 1).to_one() == 5     # True
Odds.fractional(9, 4).to_one() == 2.25  # True
Odds(3.25).to_one() == 2.25             # True  
```

There are also operators to perform calculations with Odds instances, though this is more useful in some cases than others.
For example, it is possible to calculate the combined odds of two 3/1 shots as follows:

```
Odds.fractional(3, 1) + Odds.fractional(3, 1) == Odds.evens  # True
```

### Market

A Market is a dictionary of "runners" (which can be of any type) and Odds. A market also has a places attribute. The
default for this is 1 (i.e. a win market), but it can be set to any value.

A Market can be instantiated any way a python dictionary can. Given a list of runners and odds a market can be created like this:

```
runners = ['Frankel', 'Sea The Stars', 'Brigadier Gerard', 'Dancing Brave', 'Quixall Crossett']
odds = [Odds(x) for x in [2, 4, 5, 10, 1000]]
market = Market(zip(runners, odds))
```
Alternatively, the market could be created runner by runner...

```
market = Market()
market['Frankel'] = Odds(2)
```

You may also wish to create an "empty" market, to assign odds later:
```
market = Market.fromkeys(runners)
```
Markets have a number of properties:

* ```favourites``` - a list of the shortest price runners in the market (NB: It will always be a list, even if there is only one)
* ```percentage``` - the sum of every runner's implied percentage chance
* ```overround_per_runner``` - the above, divided by the number of runners
* ```is_overbroke``` - true if the market is in the punter's favour, i.e. < 100% book, false otherwise
* ```is_overround``` - true if the market is in the bookie's favour, i.e. > 100% book, false otherwise
* ```is_fair``` - only true if the book is at exactly 100%

They also have a number of methods. The following market is used in the explanation of them:

```
market = Market({'Frankel': 2, 'Sea the Stars': 3, 'Brigadier Gerard': 6})
```

#### ```apply_margin``` 

Allows the user to manipulate the overround on a market. For example, in the 'fair' market given above, applying a margin of 20% as follows:

```
market.apply_margin(20)
```

will change the odds in the following way:

```
market.get('Frankel')           # 1.667 (to 3 dp)
market.get('Sea The Stars')     # 2.5
market.get('Brigadier Gerard')  # 5
market.percentage               # 120
```

Note that the method applies the margin in proportion to each runner's current odds.

#### ```equalise```

Resets the market to a fair market where all runners have the same odds.

```
market.equalise()
market.get('Frankel')           # 3
market.get('Sea The Stars')     # 3
market.get('Brigadier Gerard')  # 3
market.percentage               # 100
```

#### ```fill```

Fills out any missing odds in the market to the specified margin.

```
market['Frankel'] = None
market.fill(10)
market.get('Frankel')           # 1.667 (to 3 dp)
```

That is, the odds of Sea The Stars (3) and Brigadier Gerard (6) represent a 50% market. To fill out the entire market to a 10% margin requires Frankel's odds to be 60% or 1.667. If there were three unpriced runners, they'd all be set to 20% or 5.

Where no margin is specified, a 100% market is assumed.

```
market['Frankel'] = None
market.fill()
market.get('Frankel')           # 2
```

#### ```share_for```

Returns the market share for the specified horse.

```
market.share_for('Frankel')     # 50
```

#### ```wipe```

Clears the market, setting all odds to none. 

```
market.wipe()
market.get('Frankel')           # None
```

#### ```without``` 

Allows the user to extract runners from markets. In its current state, it is of little practical use, as it just
extracts the runners, normally leaving an overbroke market. In future releases, this will be enhanced to automatically recalculate.

```
market = market.without(['Frankel'])
market.favourites == ['Sea The Stars']  # True
```