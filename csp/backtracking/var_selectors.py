import copy
from abc import ABCMeta, abstractmethod
from csp_components import CSP, Variable, Assignment
import random


class VarOrderingHeuristic(metaclass=ABCMeta):

    @abstractmethod
    def __call__(self, csp: CSP[Variable[any]], assignment: Assignment) -> Variable[any]:
        pass

    def backtrack(self) -> None:
        pass


class MRVVarOrderingHeuristic(VarOrderingHeuristic):

    def __call__(self, csp: CSP[Variable[any]], assignment: Assignment) -> Variable[any]:
        mrv_by_var = {}
        for variable in csp.nodes():
            if variable in assignment:
                continue
            tot_legal_values = self._count_legal_values(csp, variable)
            mrv_by_var[variable] = tot_legal_values
        return min(mrv_by_var, key=mrv_by_var.get)

    @staticmethod
    def _count_legal_values(csp: CSP[Variable[any]], var: Variable[any]) -> int:
        tot_legal_values = 0
        for value in var.domain:
            all_adj_consistent = True
            for adj in csp.adj(var):
                constraint_var_to_adj = csp.edge_constraint(var, adj)
                constraint_adj_to_var = csp.edge_constraint(adj, var)

                adj_consistent = False
                for adj_value in adj.domain:
                    if constraint_var_to_adj(value, adj_value) and constraint_adj_to_var(value, adj_value):
                        adj_consistent = True
                        break
                if not adj_consistent:
                    all_adj_consistent = False
                    break

            if all_adj_consistent:
                tot_legal_values += 1
        return tot_legal_values


class StaticVarOrderingHeuristic(VarOrderingHeuristic):

    def __init__(self):
        self._variables = None
        self._cursor = 0

    def __call__(self, csp: CSP[Variable[any]], assignment: Assignment) -> Variable[any]:
        if self._variables is None:
            self._variables = csp.nodes()
        variable = self._variables[self._cursor]
        self._cursor += 1
        return variable

    def backtrack(self) -> None:
        self._cursor -= 1


class RandomVarOrderingHeuristics(VarOrderingHeuristic):

    def __init__(self):
        self._variables = None
        self._cursor = 0

    def __call__(self, csp: CSP[Variable[any]], assignment: Assignment) -> Variable[any]:
        if self._variables is None:
            copy_nodes = copy.deepcopy(csp.nodes())
            random.shuffle(copy_nodes)
            self._variables = copy_nodes
        variable = self._variables[self._cursor]
        self._cursor += 1
        return variable

    def backtrack(self) -> None:
        self._cursor -= 1


class DegreeVarOrderingHeuristic(VarOrderingHeuristic):

    def __call__(self, csp: CSP[Variable[any]], assignment: Assignment) -> Variable[any]:
        num_constraints_by_var = {}
        for var in csp.nodes():
            tot_constraints = 0
            if var in assignment:
                continue
            for adj in csp.adj(var):
                if adj in assignment:
                    continue
                tot_constraints += 1
            num_constraints_by_var[var] = tot_constraints
        return max(num_constraints_by_var, key=num_constraints_by_var.get)