# Backtracking Algorithm for CSP Problems
This package contains an implementation of the **Backtracking Algorithm** to solve **Constraint Satisfaction Problems (CSP)**.

## Usage Example
```python
from backtracking.backtracking_search import backtracking_search
from backtracking.var_selectors import (
    VarOrderingHeuristic,
    MRVVarOrderingHeuristic,
    StaticVarOrderingHeuristic,
    RandomVarOrderingHeuristics,
    DegreeVarOrderingHeuristic
)
from backtracking.value_selectors import (
    ValueOrderHeuristic,
    LeastConstrainingValueOrderingHeuristic,
    StaticValueOrderingHeuristic,
    RandomValueOrderingHeuristic
)
from backtracking.infereces import Inference, ArcConsistencyInference
from csp_components import CSP, Variable, Assignment
from csp_problems import map_colouring_problem, knights_chessboard_problem


if __name__ == '__main__':
    # Choose a CSP problem
    csp = knights_chessboard_problem(tot_knights=10, dim_chessboard=4)

    # Inferences
    arc_consistency_inference = ArcConsistencyInference()

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
        var_ordering_heuristic=static_var_ordering,
        value_ordering_heuristic=random_value_ordering,
        inference=arc_consistency_inference
    )

    print(f'Solution: {solution}')
```