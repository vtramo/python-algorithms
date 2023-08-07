from typing import Callable
from copy import deepcopy
from random import shuffle

from csp.csp_components import CSP, Assignment, Variable
from csp.csp_problems import knights_chessboard_problem


def min_conflicts(csp: CSP[Variable[any]],
                  max_steps: int,
                  init_assignment: Callable[[CSP[Variable[any]]], Assignment[Variable[any]]] =
                  lambda csp: _init_random_assignment(csp)
                  ) -> Assignment[Variable[any]] | bool:

    assignment = init_assignment(csp)
    for _ in range(0, max_steps):
        if assignment.is_solution():
            return assignment

        conflicted_var = _choose_random_conflicted_var(assignment)
        min_conflict_value = _min_conflicts_value(csp, conflicted_var)
        assignment.set(conflicted_var, min_conflict_value)
    return False


def _init_random_assignment(csp: CSP[Variable[any]]) -> Assignment[Variable[any]]:
    assignment = Assignment(csp, {})
    for var in csp.nodes():
        var_domain = deepcopy(var.domain)
        shuffle(var_domain)
        assignment.set(var, var_domain[0])
    return assignment


def _choose_random_conflicted_var(assignment: Assignment[Variable[any]]) -> Variable[any]:
    conflicted_vars = deepcopy(assignment.conflicted_variables())
    shuffle(conflicted_vars)
    return conflicted_vars[0]


def _min_conflicts_value(csp: CSP[Variable[any]], var: Variable[any]) -> any:
    num_conflicts_by_var_value = {}
    for var_value in var.initial_domain:
        for adj in csp.adj(var):
            constraint_var_adj = csp.edge_constraint(var, adj)
            adj_value = adj.domain[0]
            if not constraint_var_adj(var_value, adj_value):
                num_conflicts_by_var_value[var_value] = num_conflicts_by_var_value.get(var_value, 0) + 1

    items = list(num_conflicts_by_var_value.items())
    shuffle(items)
    num_conflicts_by_var_value = dict(items)
    return min(num_conflicts_by_var_value, key=num_conflicts_by_var_value.get)


if __name__ == '__main__':
    csp_problem = knights_chessboard_problem(tot_knights=5, dim_chessboard=8)

    print(min_conflicts(csp_problem, 1000))
