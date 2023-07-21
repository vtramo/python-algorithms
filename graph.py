from typing import TypeVar, Generic, Callable


T = TypeVar("T")


class Graph(Generic[T]):

    def __init__(self):
        self._adj: dict[T, list[T]] = {}
        self._edge_info: dict[tuple[T, T], tuple[int, Callable[[any, any], bool]]] = {}

    def add_node(self, node: T) -> None:
        if node in self._adj:
            raise ValueError("This node is already present!")
        self._adj[node] = []

    def add_edge(self,
                 a_node: T,
                 b_node: T,
                 cost: int = 0,
                 constraint: Callable[[any, any], bool] = lambda: True) -> None:
        a_adj = self._adj[a_node]
        a_adj.append(b_node)
        self._edge_info[(a_node, b_node)] = (cost, constraint)

    def add_bidirectional_edge(self,
                               a_node: T,
                               b_node: T, cost: int = 0,
                               constraint: Callable[[any, any], bool] = lambda: True) -> None:
        self.add_edge(a_node, b_node, cost, constraint)
        self.add_edge(b_node, a_node, cost, constraint)

    def adj(self, node: T) -> list[tuple[T]]:
        return self._adj[node]

    def edge_cost(self, a_node: T, b_node: T) -> int:
        cost, _ = self._edge_info[(a_node, b_node)]
        return cost

    def edge_constraint(self, a_node: T, b_node: T) -> Callable[[any, any], bool]:
        _, constraint = self._edge_info[(a_node, b_node)]
        return constraint

    def all_edges(self) -> list[tuple[T, T]]:
        return list(self._edge_info.keys())
