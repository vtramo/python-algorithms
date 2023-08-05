from queue import Queue

from csp.csp_components import CSP, Variable


def ac_3(csp: CSP[Variable[any]], queue: Queue = Queue()) -> bool:

    def revise(xi: Variable[any], xj: Variable[any]) -> bool:
        consistent_values = []
        constraint = csp.edge_constraint(xi, xj)
        for i in xi.domain:
            for j in xj.domain:
                if constraint(i, j):
                    consistent_values.append(i)
                    break
        revised = len(xi.domain) != len(consistent_values)
        xi.domain = consistent_values
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
    csp = CSP[Variable[int]]()

    A = Variable[int](domain=[1])
    B = Variable[int](domain=[1])
    C = Variable[int](domain=[1, 2, 3])
    D = Variable[int](domain=[1, 2, 3])
    E = Variable[int](domain=[1, 2, 3])
    F = Variable[int](domain=[1, 2, 3])

    csp.add_node(A)
    csp.add_node(B)
    csp.add_node(C)
    csp.add_node(D)
    csp.add_node(E)
    csp.add_node(F)

    csp.add_bidirectional_edge(A, B, constraint=lambda a, b: a != b)
    csp.add_bidirectional_edge(A, D, constraint=lambda a, d: a != d)
    csp.add_bidirectional_edge(A, C, constraint=lambda a, c: a != c)
    csp.add_bidirectional_edge(B, C, constraint=lambda b, c: b != c)
    csp.add_bidirectional_edge(B, E, constraint=lambda b, e: b != e)
    csp.add_bidirectional_edge(C, F, constraint=lambda c, f: c != f)

    print(ac_3(csp))
