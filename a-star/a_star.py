from __future__ import annotations

from graph import Graph
from dataclasses import dataclass, field
from queue import PriorityQueue


@dataclass(slots=True, order=True)
class Node:
    state: str = field(compare=False)
    cost: int = field(default=0)
    parent: Node = field(default=None, compare=False)


@dataclass(slots=True)
class Problem:
    initial_node: Node
    goal_state: str
    graph: Graph[str]
    heuristics: dict[str, int]

    def is_goal(self, state: str) -> bool:
        return state == self.goal_state


counter = 0


def a_star(problem: Problem) -> Node | None:
    global counter
    graph = problem.graph
    initial_node = problem.initial_node

    def expand(node: Node) -> list[Node]:
        for adj_state in graph.adj(node.state):
            cost = node.cost + graph.edge_cost(node.state, adj_state)
            cost += problem.heuristics[adj_state] - problem.heuristics[node.state]
            yield Node(state=adj_state, parent=node, cost=cost)

    frontier = PriorityQueue[Node]()
    frontier.put_nowait(initial_node)
    reached = {initial_node.state: initial_node}
    while not frontier.empty():
        counter += 1
        node = frontier.get_nowait()
        if problem.is_goal(node.state):
            return node
        for adj in expand(node):
            adj_state = adj.state
            if adj_state not in reached or adj.cost < reached[adj_state].cost:
                reached[adj_state] = adj
                frontier.put_nowait(adj)


if __name__ == '__main__':
    graph = Graph[str]()

    graph.add_node('A')
    graph.add_node('B')
    graph.add_node('C')
    graph.add_node('D')
    graph.add_node('E')
    graph.add_node('F')
    graph.add_node('G')

    graph.add_bidirectional_edge('A', 'B', cost=1)
    graph.add_bidirectional_edge('A', 'C', cost=4)
    graph.add_bidirectional_edge('B', 'C', cost=1)
    graph.add_bidirectional_edge('B', 'D', cost=5)
    graph.add_bidirectional_edge('C', 'D', cost=3)
    graph.add_bidirectional_edge('D', 'E', cost=8)
    graph.add_bidirectional_edge('D', 'G', cost=9)
    graph.add_bidirectional_edge('D', 'F', cost=3)
    graph.add_bidirectional_edge('E', 'G', cost=2)
    graph.add_bidirectional_edge('D', 'G', cost=9)
    graph.add_bidirectional_edge('F', 'G', cost=5)

    heuristics1 = {
        'A': 9.5,
        'B': 9,
        'C': 8,
        'D': 7,
        'E': 1.5,
        'F': 4,
        'G': 0
    }

    heuristics2 = {
        'A': 10,
        'B': 12,
        'C': 10,
        'D': 8,
        'E': 1,
        'F': 4.5,
        'G': 0
    }

    initial_node = Node(state='A', cost=heuristics1['A'])
    problem = Problem(initial_node=initial_node, goal_state='G', graph=graph, heuristics=heuristics1)

    print(a_star(problem))
    print(counter)
