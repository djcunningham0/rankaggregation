from operator import itemgetter


def sort_by_value(d, reverse=False):
    """
    Sort a dictionary by value.
    """
    return sorted(d.items(), key=itemgetter(1), reverse=reverse)
