from __future__ import annotations

import copy
import uuid
from graph import Graph
from dataclasses import dataclass, field
from typing import TypeVar, Generic, Callable
from uuid import uuid4

D = TypeVar("D")


@dataclass(slots=True)
class Variable(Generic[D]):
    domain: list[D]
    unary_constraints: list[Callable[[D], bool]] = field(default_factory=lambda: [])
    id: str = ''
    name: str = ''

    def __post_init__(self) -> None:
        self.id = uuid4()
        self.name = self.id if not self.name else self.name

    def __hash__(self) -> int:
        return self.id.__hash__()

    def __str__(self) -> str:
        return self.name.__str__()

    def __eq__(self, other: Variable[D]) -> bool:
        return self.id == other.id


class Assignment(Generic[D]):

    def __init__(self, csp: CSP, assignment: dict[Variable[D], D]):
        self._assignment: dict[Variable[D], (list[D], D)] = {}
        self._csp = csp
        for var, value in assignment.items():
            self.add(var, value)

    def add(self, var: Variable[any], value: any) -> None:
        backup_var_domain = copy.deepcopy(var.domain)
        self._assignment[var] = (backup_var_domain, value)
        var.domain = [value]

    def remove(self, var: Variable[any]) -> None:
        backup_var_domain, _ = self._assignment[var]
        del self._assignment[var]
        var.domain = backup_var_domain

    def is_consistent_value(self, var: Variable[any], value: any) -> bool:
        if len(self._assignment) == 0:
            return True

        all_edges = self._csp.edges()
        for assigned_var in self._assignment.keys():
            if (var, assigned_var) not in all_edges:
                continue
            constraint_var_to_assigned_var = self._csp.edge_constraint(var, assigned_var)
            constraint_assigned_var_to_var = self._csp.edge_constraint(assigned_var, var)
            _, assigned_var_value = self._assignment[assigned_var]
            if not constraint_var_to_assigned_var(value, assigned_var_value) \
                    or not constraint_assigned_var_to_var(assigned_var_value, value):
                return False

        return True

    def __len__(self) -> int:
        return len(self._assignment)

    def __contains__(self, variable: Variable[any]):
        return variable in self._assignment.keys()

    def __str__(self) -> str:
        assigned_vars: dict[str, str] = {}
        for var, (backup_domain, assigned_value) in self._assignment.items():
            assigned_vars[var.__str__()] = assigned_value.__str__()
        return assigned_vars.__str__()


class CSP(Graph[Variable[D]]):
    ARCH_CONSTRAINT_KEY = 'constraint'

    def add_edge(self,
                 a_var: Variable[D],
                 b_var: Variable[D],
                 cost: int = 0,
                 constraint: Callable[[Variable[D], Variable[D]], bool] = lambda: True) -> None:
        super().add_edge(a_var, b_var, cost)
        edge_info = self._edge_info[(a_var, b_var)]
        edge_info[self.ARCH_CONSTRAINT_KEY] = constraint

    def add_bidirectional_edge(self,
                               a_var: Variable[D],
                               b_var: Variable[D],
                               cost: int = 0,
                               constraint: Callable[[Variable[D], Variable[D]], bool] = lambda: True) -> None:
        self.add_edge(a_var, b_var, cost, constraint)
        self.add_edge(b_var, a_var, cost, lambda b, a: constraint(a, b))

    def edge_constraint(self, a_var: Variable[D], b_var: Variable[D]) -> Callable[[Variable[D], Variable[D]], bool] | None:
        try:
            edge_info = self._edge_info[(a_var, b_var)]
        except KeyError:
            return None
        return edge_info[self.ARCH_CONSTRAINT_KEY]

    def backup_var_domains(self) -> dict[Variable[D], list[D]]:
        backup_var_domains = {}
        for variable in self._adj.keys():
            backup_var_domains[variable] = copy.deepcopy(variable.domain)
        return backup_var_domains

    def restore_var_domains(self, backup_var_domains: dict[Variable[any], list[any]]) -> None:
        for variable in self._adj.keys():
            variable.domain = backup_var_domains[variable]
