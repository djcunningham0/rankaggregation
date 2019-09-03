rankaggretation
===============

This package implements some rank aggregation methods in Python. Currently, the
following methods are supported:

* Instant Runoff Voting
* Borda count
* Dowdall system (variant of Borda count)
* "Average rank" -- just take the average rank of each item across all lists. I
  don't know if there is a real name for this method.

I plan on adding additional methods in the future (such as the Markov chain
methods described in `this paper 
<http://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.28.8702&rep=rep1&type=pdf>`_.

All methods currently implemented are designed to work with partial lists (i.e.,
each base ranker does not necessarily rank every item).

Installation
------------

Install from PyPI:

``pip install rankaggregation``


Example usage
-------------

The key object in the package is the ``RankAggregator`` class. Each method takes
``rank_list`` as a parameter. Each list in ``rank_list`` is the ranking preference
of a single base ranker.

>>> import rankaggregation as ra
>>> agg = ra.RankAggregator()
>>> rank_list = [['A', 'B', 'C'], ['B', 'A', 'C'], ['C', 'D', 'A']]
>>> agg.instant_runoff(rank_list)
['A', 'B', 'C', 'D']
>>> agg.borda(rank_list)
[('A', 9), ('B', 8.0), ('C', 8), ('D', 5.0)]
>>> agg.dowdall(rank_list)
[('A', 1.8333333333333333), ('C', 1.6666666666666665), ('B', 1.5), ('D', 0.5)]
>>> agg.average_rank(rank_list)
[('B', 1.5), ('A', 2.0), ('D', 2.0), ('C', 2.3333333333333335)]
