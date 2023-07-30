import copy
from csp.csp_components import CSP, Variable


def map_colouring_problem() -> CSP[Variable[str]]:
    csp = CSP[Variable[str]]()

    domain = ['red', 'green', 'blue']

    WA = Variable[str](domain=copy.copy(domain), name='WA')
    NT = Variable[str](domain=copy.copy(domain), name='NT')
    SA = Variable[str](domain=copy.copy(domain), name='SA')
    Q = Variable[str](domain=copy.copy(domain), name='Q')
    NSW = Variable[str](domain=copy.copy(domain), name='NSW')
    V = Variable[str](domain=copy.copy(domain), name='V')
    T = Variable[str](domain=copy.copy(domain), name='T')

    csp.add_node(SA)
    csp.add_node(WA)
    csp.add_node(NSW)
    csp.add_node(Q)
    csp.add_node(V)
    csp.add_node(NT)
    csp.add_node(T)

    def constraint(a, b): return a != b

    csp.add_bidirectional_edge(WA, NT, constraint=constraint)
    csp.add_bidirectional_edge(WA, SA, constraint=constraint)
    csp.add_bidirectional_edge(NT, SA, constraint=constraint)
    csp.add_bidirectional_edge(NT, Q, constraint=constraint)
    csp.add_bidirectional_edge(SA, Q, constraint=constraint)
    csp.add_bidirectional_edge(SA, NSW, constraint=constraint)
    csp.add_bidirectional_edge(Q, NSW, constraint=constraint)
    csp.add_bidirectional_edge(V, NSW, constraint=constraint)
    csp.add_bidirectional_edge(SA, V, constraint=constraint)

    return csp


def knights_chessboard_problem(tot_knights: int, dim_chessboard: int) -> CSP[Variable[tuple[int, int]]]:
    positions = [(i, j) for i in range(0, dim_chessboard) for j in range(0, dim_chessboard)]
    csp = CSP[Variable[tuple[int, int]]]()
    for k in range(0, tot_knights):
        knight = Variable[tuple[int, int]](domain=copy.copy(positions), name=f'Knight{k}')
        csp.add_node(knight)

    def constraint(knight1_pos: tuple[int, int], knight2_pos: tuple[int, int]) -> bool:
        if knight1_pos == knight2_pos:
            return False

        knight1_moves = [
            (knight1_pos[0] + 1, knight1_pos[1] + 3),
            (knight1_pos[0] - 1, knight1_pos[1] + 3),
            (knight1_pos[0] + 3, knight1_pos[1] + 1),
            (knight1_pos[0] + 3, knight1_pos[1] - 1),
            (knight1_pos[0] + 1, knight1_pos[1] - 3),
            (knight1_pos[0] - 1, knight1_pos[1] - 3),
            (knight1_pos[0] - 3, knight1_pos[1] + 1),
            (knight1_pos[0] - 3, knight1_pos[1] - 1),
        ]

        for x, y in knight1_moves:
            if x < 0 or x >= dim_chessboard or y < 0 or y >= dim_chessboard:
                continue
            if (x, y) == knight2_pos:
                return False

        return True

    for knight1 in csp.nodes():
        for knight2 in csp.nodes():
            if knight1 == knight2:
                continue
            csp.add_edge(knight1, knight2, constraint=constraint)

    return csp
