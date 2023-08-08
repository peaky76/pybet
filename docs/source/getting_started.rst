Getting started
---------------

The key components of pybet are: 

The Odds class which enables conversion from and to the following types of odds or odds-equivalent:

- Decimal odds, e.g. 2.5
- Fractional odds, e.g. 6/4
- American moneyline odds, e.g. +150
- Implied percentage, e.g. 40
- Implied probability, e.g. 0.4

A Market class which allows for the creation of markets based on those odds and some limited calculations on those markets

For a basic guide to odds, please see [https://www.investopedia.com/articles/investing/042115/betting-basics-fractional-decimal-american-moneyline-odds.asp]

Odds
^^^^

Internally, the value of an Odds instance is stored as a Decimal, making decimal odds the effective default.
Odds can be instantiated directly as decimals or via a class method, specifying the type of odds being instantiated from.
Any Odds instance can then be output to any type with a to\_{type} method, e.g.

.. code-block:: python

   from pybet import Odds

   o = Odds(2.5)
   o.to_moneyline()    # +150
   o.to_percentage()   # 40

   o = Odds.fractional(6, 4)
   o.to_probability()  # 0.4

The to_fractional() method requires a set of fractional odds to work from. It will then select the closest matching value
from that set. For convenience, a set of standard odds, representing those most typically found in the UK, has been provided.

.. code-block:: python

   o.to_fractional('5/4', '6/4', '7/4', '2/1') # 6/4
   o.to_fractional(FractionalOddsSets.STANDARD) # 6/4


Comparisons can be made between Odds instances. It is possible to check if one Odds instance is shorter (<)
or longer (>) than another, e.g.


.. code-block:: python

   Odds(2.5) < Odds.fractional(11, 4)        # True
   Odds.probability(50) > Odds(3)            # False


There are properties to compare Odds instances to evens, and a convenience method for evens itself, e.g.

.. code-block:: python

   o.is_odds_against   # True
   o.is_odds_on        # True
   Odds.evens() == 2   # True

It is possible to invert odds, to turn odds against into the equivalent odds on value and vice versa, e.g.

.. code-block:: python

   Odds.inverted(2.5) == Odds.fractional(4, 6)  # True

It is also possible to get the odds "to one" i.e. the numerator of fractional odds, but with a decimal numerator if that is applicable,
or, put another way, the fractional odds with the stake removed.

.. code-block:: python

   Odds.fractional(5, 1).to_one() == 5     # True
   Odds.fractional(9, 4).to_one() == 2.25  # True
   Odds(3.25).to_one() == 2.25             # True

There are also operators to perform calculations with Odds instances, though this is more useful in some cases than others.
For example, it is possible to calculate the combined odds of two 3/1 shots as follows:

.. code-block:: python

   Odds.fractional(3, 1) + Odds.fractional(3, 1) == Odds.evens  # True

Market
^^^^^^

A Market is a dictionary of "runners" (which can be of any type) and Odds. A market also has a places attribute. The
default for this is 1 (i.e. a win market), but it can be set to any value.

A Market can be instantiated any way a python dictionary can. Given a list of runners and odds a market can be created like this:

.. code-block:: python

   runners = ['Frankel', 'Sea The Stars', 'Brigadier Gerard', 'Dancing Brave', 'Quixall Crossett']
   odds = [Odds(x) for x in [2, 4, 5, 10, 1000]]
   market = Market(zip(runners, odds))

Alternatively, the market could be created runner by runner...

.. code-block:: python

   market = Market()
   market['Frankel'] = Odds(2)

You may also wish to create an "empty" market, to assign odds later:

.. code-block:: python

   market = Market.fromkeys(runners)

Markets have a number of properties:

- `favourites` - a list of the shortest price runners in the market (NB: It will always be a list, even if there is only one)
- `percentage` - the sum of every runner's implied percentage chance
- `overround_per_runner` - the above, divided by the number of runners
- `is_overbroke` - true if the market is in the punter's favour, i.e. < 100% book, false otherwise
- `is_overround` - true if the market is in the bookie's favour, i.e. > 100% book, false otherwise
- `is_fair` - only true if the book is at exactly 100%

They also have a number of methods. The following market is used in the explanation of them:

.. code-block:: python

   market = Market({'Frankel': 2, 'Sea the Stars': 3, 'Brigadier Gerard': 6})


`apply_margin`
""""""""""""""

Allows the user to manipulate the overround on a market. For example, in the 'fair' market given above, applying a margin of 20% as follows:

.. code-block:: python

   market.apply_margin(20)


will change the odds in the following way:

.. code-block:: python

   market.get('Frankel')           # 1.667 (to 3 dp)
   market.get('Sea The Stars')     # 2.5
   market.get('Brigadier Gerard')  # 5
   market.percentage               # 120

Note that the method applies the margin in proportion to each runner's current odds.

`equalise`
""""""""""

Resets the market to a fair market where all runners have the same odds.

.. code-block:: python

   market.equalise()
   market.get('Frankel')           # 3
   market.get('Sea The Stars')     # 3
   market.get('Brigadier Gerard')  # 3
   market.percentage               # 100

`fill`
""""""

Fills out any missing odds in the market to the specified margin.

.. code-block:: python

   market['Frankel'] = None
   market.fill(10)
   market.get('Frankel')           # 1.667 (to 3 dp)

That is, the odds of Sea The Stars (3) and Brigadier Gerard (6) represent a 50% market. To fill out the entire market to a 10% margin requires Frankel's odds to be 60% or 1.667. If there were three unpriced runners, they'd all be set to 20% or 5.

Where no margin is specified, a 100% market is assumed.

.. code-block:: python

   market['Frankel'] = None
   market.fill()
   market.get('Frankel')           # 2

`meld`
""""""

Melds the market with another market, with optional weighting. Each market is normalised to 100 percent before merging

.. code-block:: python

   other_market = Market({'Frankel': 3, 'Sea the Stars': 3, 'Brigadier Gerard': 3})
 
   new_market = market.meld(other_market)
   new_market.get('Sea the Stars')     # 3
   new_market.get('Brigadier Gerard')  # 4

   new_market = market.meld(other_market, 100)
   new_market.get('Sea the Stars')     # 3
   new_market.get('Brigadier Gerard')  # 3 (i.e. the weighting is 100 percent towards the other market)


`wipe`
""""""

Clears the market, setting all odds to none.

.. code-block:: python

   market.wipe()
   market.get('Frankel')           # None

`without`
"""""""""

Allows the user to extract runners from markets. In its current state, it is of little practical use, as it just
extracts the runners, normally leaving an overbroke market. In future releases, this will be enhanced to automatically recalculate.

.. code-block:: python

   market = market.without(['Frankel'])
   market.favourites == ['Sea The Stars']  # True

Staking
^^^^^^^

The `staking` module contains methods for calculating stakes for a given set of odds and bank size.

`kelly`
"""""""

This method calculates the correct stake according to the [Kelly Criterion](https://www.investopedia.com/articles/investing/042115/betting-basics-fractional-decimal-american-moneyline-odds.asp) for a given bank size. If the odds are in the bettor's favour, this will be positive.
If they aren't the method will return zero.

.. code-block:: python
      
   kelly(Odds(4), Odds(5), 100)   # 6.25
   kelly(Odds(5), Odds(4), 100)   # 0