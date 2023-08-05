from abc import ABCMeta, abstractmethod
from copy import deepcopy
from queue import Queue

from csp.ac_3 import ac_3
from csp.csp_components import CSP, Variable


class Inference(metaclass=ABCMeta):

    @abstractmethod
    def __call__(self, csp: CSP[Variable[any]], var: Variable[any], assignment: dict[Variable[any], any]) -> bool:
        pass


class ArcConsistencyInference(Inference):

    def __call__(self, csp: CSP[Variable[any]], var: Variable[any], assignment: dict[Variable[any], any]) -> bool:
        return ac_3(csp)


class ForwardChecking(Inference):

    def __call__(self, csp: CSP[Variable[any]], var: Variable[any], assignment: dict[Variable[any], any]) -> bool:
        if len(var.domain) != 1:
            raise ValueError

        var_value = var.domain[0]
        for adj in csp.adj(var):
            if adj in assignment:
                continue
            constraint_adj_to_var = csp.edge_constraint(adj, var)

            new_adj_domain = deepcopy(adj.domain)
            for adj_value in adj.domain:
                if not constraint_adj_to_var(adj_value, var_value):
                    new_adj_domain.remove(adj_value)
                    if len(new_adj_domain) == 0:
                        return False

        return True


class MaintainingArcConsistency(Inference):

    def __call__(self, csp: CSP[Variable[any]], var: Variable[any], assignment: dict[Variable[any], any]) -> bool:
        if len(var.domain) != 1:
            raise ValueError

        queue = Queue()
        for adj in csp.adj(var):
            if adj not in assignment:
                queue.put_nowait((adj, var))

        return ac_3(csp, queue)
