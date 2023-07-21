from graph import Graph
from csp_components import Variable
from queue import Queue
import copy


def ac_3(graph: Graph[Variable[any]]) -> bool:

    def revise(xi: Variable[any], xj: Variable[any]) -> bool:
        consistent_values = []
        constraint = graph.edge_constraint(xi, xj)
        for i in xi.domain:
            for j in xj.domain:
                if constraint(i, j):
                    consistent_values.append(i)
                    break
        revised = len(xi.domain) != len(consistent_values)
        xi.domain = consistent_values
        return revised

    queue = Queue()
    for edge in graph.all_edges():
        queue.put_nowait(edge)

    while not queue.empty():
        (xi, xj) = queue.get_nowait()
        if revise(xi, xj):
            if len(xi.domain) == 0:
                return False
            for xk in graph.adj(xi):
                queue.put_nowait((xk, xi))

    return True


if __name__ == '__main__':
    graph = Graph[Variable[int]]()

    A = Variable[int](domain=[1])
    B = Variable[int](domain=[1])
    C = Variable[int](domain=[1, 2, 3])
    D = Variable[int](domain=[1, 2, 3])
    E = Variable[int](domain=[1, 2, 3])
    F = Variable[int](domain=[1, 2, 3])

    graph.add_node(A)
    graph.add_node(B)
    graph.add_node(C)
    graph.add_node(D)
    graph.add_node(E)
    graph.add_node(F)

    graph.add_bidirectional_edge(A, B, constraint=lambda a, b: a != b)
    graph.add_bidirectional_edge(A, D, constraint=lambda a, d: a != d)
    graph.add_bidirectional_edge(A, C, constraint=lambda a, c: a != c)
    graph.add_bidirectional_edge(B, C, constraint=lambda b, c: b != c)
    graph.add_bidirectional_edge(B, E, constraint=lambda b, e: b != e)
    graph.add_bidirectional_edge(C, F, constraint=lambda c, f: c != f)

    print(ac_3(graph))
