from queue import Queue

from csp.csp_components import CSP, Variable


def ac_3(csp: CSP[Variable[any]], queue: Queue = Queue()) -> bool:

    def revise(x: Variable[any], y: Variable[any]) -> bool:
        consistent_values = []
        constraint = csp.edge_constraint(x, y)
        for i in x.domain:
            for j in y.domain:
                if constraint(i, j):
                    consistent_values.append(i)
                    break
        revised = len(x.domain) != len(consistent_values)
        x.domain = consistent_values
        return revised

    if queue.empty():
        for edge in csp.edges():
            queue.put_nowait(edge)

    while not queue.empty():
        (xi, xj) = queue.get_nowait()
        if revise(xi, xj):
            if len(xi.domain) == 0:
                return False
            for xk in csp.adj(xi):
                queue.put_nowait((xk, xi))

    return True


if __name__ == '__main__':
    csp_problem = CSP[Variable[int]]()

    A = Variable[int](domain=[1])
    B = Variable[int](domain=[1])
    C = Variable[int](domain=[1, 2, 3])
    D = Variable[int](domain=[1, 2, 3])
    E = Variable[int](domain=[1, 2, 3])
    F = Variable[int](domain=[1, 2, 3])

    csp_problem.add_node(A)
    csp_problem.add_node(B)
    csp_problem.add_node(C)
    csp_problem.add_node(D)
    csp_problem.add_node(E)
    csp_problem.add_node(F)

    csp_problem.add_bidirectional_edge(A, B, constraint=lambda a, b: a != b)
    csp_problem.add_bidirectional_edge(A, D, constraint=lambda a, d: a != d)
    csp_problem.add_bidirectional_edge(A, C, constraint=lambda a, c: a != c)
    csp_problem.add_bidirectional_edge(B, C, constraint=lambda b, c: b != c)
    csp_problem.add_bidirectional_edge(B, E, constraint=lambda b, e: b != e)
    csp_problem.add_bidirectional_edge(C, F, constraint=lambda c, f: c != f)

    print(ac_3(csp_problem))
