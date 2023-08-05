from abc import ABCMeta, abstractmethod
from csp_components import CSP, Variable, Assignment
from csp_problems import map_colouring_problem, knights_chessboard_problem
from infereces import Inference, ArcConsistencyInference, ForwardChecking, MaintainingArcConsistency
from var_selectors import (
    VarOrderingHeuristic,
    MRVVarOrderingHeuristic,
    StaticVarOrderingHeuristic,
    RandomVarOrderingHeuristics,
    DegreeVarOrderingHeuristic
)
from value_selectors import (
    ValueOrderHeuristic,
    LeastConstrainingValueOrderingHeuristic,
    StaticValueOrderingHeuristic,
    RandomValueOrderingHeuristic
)


def backtracking_search(csp: CSP[Variable[any]],
                        inference: Inference,
                        var_ordering_heuristic: VarOrderingHeuristic,
                        value_ordering_heuristic: ValueOrderHeuristic) -> Assignment[any]:

    def backtrack(assignment: Assignment) -> dict[Variable[any], any]:
        print(f'- {assignment}')

        if len(assignment) == len(csp):
            return assignment

        var = var_ordering_heuristic(csp, assignment)
        values = value_ordering_heuristic(csp, var, assignment)
        for step, value in enumerate(start=1, iterable=values):
            if assignment.is_consistent_value(var, value):
                assignment.add(var, value)
                backup_var_domains = csp.backup_var_domains()

                inferences = inference(csp, var, assignment)
                if inferences is not False:
                    result = backtrack(assignment)
                    if result is not False:
                        return assignment
                    csp.restore_var_domains(backup_var_domains)

                assignment.remove(var)

        var_ordering_heuristic.backtrack()
        return False

    assignment = Assignment(csp, assignment={})
    return backtrack(assignment)


if __name__ == '__main__':
    # Choose a CSP problem
    csp = knights_chessboard_problem(tot_knights=10, dim_chessboard=4)

    # Inferences
    arc_consistency_inference = ArcConsistencyInference()
    forward_checking = ForwardChecking()
    maintaining_arc_consistency = MaintainingArcConsistency()

    # Variable Ordering Heuristics
    mrv_var_ordering = MRVVarOrderingHeuristic()
    degree_var_ordering = DegreeVarOrderingHeuristic()
    static_var_ordering = StaticVarOrderingHeuristic()
    random_var_ordering = RandomVarOrderingHeuristics()

    # Value Ordering Heuristics
    least_constraining_value_ordering = LeastConstrainingValueOrderingHeuristic()
    static_value_ordering = StaticValueOrderingHeuristic()
    random_value_ordering = RandomValueOrderingHeuristic()

    # Compute solution
    solution = backtracking_search(
        csp=csp,
        var_ordering_heuristic=mrv_var_ordering,
        value_ordering_heuristic=least_constraining_value_ordering,
        inference=maintaining_arc_consistency
    )

    print(f'Solution: {solution}')
