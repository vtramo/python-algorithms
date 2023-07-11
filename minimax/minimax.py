from __future__ import annotations
from dataclasses import dataclass, field


class TreeNode:

    def __init__(self, state: str):
        self.children: list[TreeNode] = []
        self.state: str = state

    def add_child(self, node: TreeNode) -> None:
        if node in self.children:
            raise ValueError
        self.children.append(node)


@dataclass(slots=True)
class Game:
    terminal_states: dict[str, int]

    def is_terminal(self, state: str) -> bool:
        return state in self.terminal_states

    def utility(self, state: str) -> int:
        return self.terminal_states[state]


def alpha_beta_search(game: Game, node: TreeNode) -> int:
    def max_value(node: TreeNode, alpha: int, beta: int) -> int:
        if game.is_terminal(node.state):
            return game.utility(node.state)

        v = float('-inf')

        for child in node.children:
            print(f'{child.state} visited.')
            v2 = min_value(child, alpha, beta)
            if v2 > v:
                v = v2
                alpha = max(alpha, v)
            if v >= beta:
                return v

        return v

    def min_value(node: TreeNode, alpha: int, beta: int) -> int:
        if game.is_terminal(node.state):
            return game.utility(node.state)

        v = float('inf')

        for child in node.children:
            print(f'{child.state} visited.')
            v2 = max_value(child, alpha, beta)
            if v2 < v:
                v = v2
                beta = min(beta, v)
            if v <= alpha:
                return v

        return v

    return max_value(node, float('-inf'), float('inf'))


if __name__ == '__main__':
    root = TreeNode('A')
    B = TreeNode('B')
    C = TreeNode('C')
    D = TreeNode('D')
    E = TreeNode('E')
    F = TreeNode('F')
    G = TreeNode('G')
    H = TreeNode('H')
    I = TreeNode('I')
    L = TreeNode('L')
    M = TreeNode('M')
    N = TreeNode('N')
    O = TreeNode('O')
    P = TreeNode('P')
    Q = TreeNode('Q')

    root.add_child(B)
    root.add_child(C)

    B.add_child(D)
    B.add_child(E)

    C.add_child(F)
    C.add_child(G)

    D.add_child(H)
    D.add_child(I)

    E.add_child(L)
    E.add_child(M)

    F.add_child(N)
    F.add_child(O)

    G.add_child(P)
    G.add_child(Q)

    terminal_state = {
        'H': 1,
        'I': 3,
        'L': 2,
        'M': -1,
        'N': 4,
        'O': -2,
        'P': 1,
        'Q': -1
    }

    game = Game(terminal_state)

    print(f'utility: {alpha_beta_search(game, root)}')
