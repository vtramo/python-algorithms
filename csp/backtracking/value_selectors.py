from abc import ABCMeta, abstractmethod
from csp_components import CSP, Variable
import copy
import random


class ValueOrderHeuristic(metaclass=ABCMeta):

    @abstractmethod
    def __call__(self, csp: CSP[Variable[any]], var: Variable[any], assignment: dict[Variable[any], any]) -> list[any]:
        pass


class LeastConstrainingValueOrderingHeuristic(ValueOrderHeuristic):

    def __call__(self, csp: CSP[Variable[any]], var: Variable[any], assignment: dict[Variable[any], any]) -> list[any]:
        score_by_value = {}
        for value in var.domain:
            value_score = 0
            for adj in csp.adj(var):
                for adj_value in adj.domain:
                    constraint_adj_to_var = csp.edge_constraint(adj, var)
                    if constraint_adj_to_var(adj_value, value):
                        value_score += 1
            score_by_value[value] = value_score
        return sorted(score_by_value, key=lambda dict_key: score_by_value[dict_key], reverse=True)


class StaticValueOrderingHeuristic(ValueOrderHeuristic):

    def __call__(self, csp: CSP[Variable[any]], var: Variable[any], assignment: dict[Variable[any], any]) -> list[any]:
        return var.domain


class RandomValueOrderingHeuristic(ValueOrderHeuristic):

    def __call__(self, csp: CSP[Variable[any]], var: Variable[any], assignment: dict[Variable[any], any]) -> list[any]:
        copy_var_domain = copy.deepcopy(var.domain)
        random.shuffle(copy_var_domain)
        return copy_var_domain
