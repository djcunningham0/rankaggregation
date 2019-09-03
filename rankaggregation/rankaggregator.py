import numpy as np
import rankaggregation.utils as utils


class RankAggregator(object):
    def __init__(self):
        pass

    def _get_rank_dict(self, rank_list):
        item_ranks = {}.fromkeys(set().union(*rank_list))
        for i in item_ranks:
            item_ranks[i] = [x.index(i)+1 for x in rank_list if i in x]  # add 1 so ranks start from 1

        return item_ranks

    def average_rank(self, rank_list):
        rank_dict = self._get_rank_dict(rank_list)
        agg_dict = {}
        for i in rank_dict:
            agg_dict[i] = np.mean(rank_dict[i])

        return utils.sort_by_value(agg_dict)

    def _get_count_dict(self, rank_list):
        """
        Count the number of 1st-place votes for each candidate.

        :param rank_list: list where each element is a list of ranks (e.g., [['a', 'b', 'c'], ['b', 'a', 'c']])
        :return: dictionary with pairs of candidate: vote count
        """
        first_choices = [x[0] for x in rank_list if len(x) > 0]
        counts = {}.fromkeys(set().union(*rank_list), 0)
        for i in set(first_choices):
            counts[i] = first_choices.count(i)

        return utils.sort_by_value(counts, reverse=True)

    def _drop_candidates(self, rank_list, candidates):
        if isinstance(candidates, str):
            candidates = [candidates]
        elif not isinstance(candidates, list):
            raise ValueError('candidates must be a list or string')

        for i, lst in enumerate(rank_list):
            rank_list[i] = [x for x in lst if x not in candidates]

        return rank_list

    def _irv(self, rank_list):
        _rank_list = [x for x in rank_list if len(x) > 0].copy()
        n_voters = len(_rank_list)
        counts = self._get_count_dict(_rank_list)
        if len(counts) == 1:
            # this is an edge case that happens when we have partial lists and a candidate never reaches
            # a majority -- not 100% sure I'm handling it correctly
            return counts[0][0]
        if counts[0][1] > n_voters / 2:
            winner = counts[0][0]
            return winner
        else:
            # reassign first place votes and rerun
            eliminated_candidates = [x[0] for x in counts if x[1] == 0]  # no first place votes
            counts = [x for x in counts if x[1] > 0]
            eliminated_candidates.append(counts[-1][0])  # fewest first place votes among remaining candidates
            _rank_list = self._drop_candidates(_rank_list, eliminated_candidates)
            return self._irv(_rank_list)

    def instant_runoff(self, rank_list):
        rank_list = rank_list.copy()
        n_candidates = len(set().union(*rank_list))
        final_list = []

        # repeatedly run IRV procedure (drop first winner to get second place, and so on)
        while len(final_list) < n_candidates:
            winner = self._irv(rank_list)
            final_list.append(winner)
            rank_list = self._drop_candidates(rank_list, candidates=winner)

        return final_list

    def borda(self, rank_list, min_score=1, unranked='split'):
        if min_score < 0:
            raise ValueError('min_score must be greater than zero')
        elif unranked not in ['split', 'min']:
            raise ValueError("unranked method must be one of ['split', 'min']")

        all_candidates = set().union(*rank_list)
        n_candidates = len(all_candidates)
        scores = {}.fromkeys(all_candidates, 0)
        for candidate in all_candidates:
            for lst in rank_list:
                if candidate in lst:
                    scores[candidate] += (n_candidates - lst.index(candidate) - 1 + min_score)
                elif unranked == 'split':
                    # split points evenly among unranked candidates
                    scores[candidate] += (sum(range(n_candidates - len(lst) + min_score))) / (n_candidates - len(lst))
                elif unranked == 'min':
                    # all unranked candidates get minimum score
                    scores[candidate] += min_score
                else:
                    # should never reach this point if input validation is done correctly
                    raise ValueError('invalid value for unranked parameter')

        return utils.sort_by_value(scores, reverse=True)

    def dowdall(self, rank_list):
        all_candidates = set().union(*rank_list)
        scores = {}.fromkeys(all_candidates, 0)
        for lst in rank_list:
            for i, candidate in enumerate(lst):
                scores[candidate] += 1 / (i + 1)

        return utils.sort_by_value(scores, reverse=True)
