from typing import TypeVar, Generic, Callable


T = TypeVar("T")


class Graph(Generic[T]):
    ARCH_COST_KEY = 'cost'

    def __init__(self):
        self._adj: dict[T, list[T]] = {}
        self._edge_info: dict[tuple[T, T], dict[str, any]] = {}

    def add_node(self, node: T) -> None:
        if node in self._adj:
            raise ValueError("This node is already present!")
        self._adj[node] = []

    def add_edge(self,
                 a_node: T,
                 b_node: T,
                 cost: int = 0) -> None:
        a_adj = self._adj[a_node]
        a_adj.append(b_node)

        self._edge_info.setdefault((a_node, b_node), {})
        edge_info = self._edge_info[(a_node, b_node)]
        edge_info[self.ARCH_COST_KEY] = cost

    def add_bidirectional_edge(self,
                               a_node: T,
                               b_node: T, cost: int = 0) -> None:
        self.add_edge(a_node, b_node, cost)
        self.add_edge(b_node, a_node, cost)

    def adj(self, node: T) -> list[tuple[T]]:
        return self._adj[node]

    def edge_cost(self, a_node: T, b_node: T) -> int:
        edge_info = self._edge_info[(a_node, b_node)]
        return edge_info[self.ARCH_COST_KEY]

    def nodes(self) -> list[T]:
        return list(self._adj.keys())

    def edges(self) -> list[tuple[T, T]]:
        return list(self._edge_info.keys())

    def __len__(self) -> int:
        return len(self._adj)
