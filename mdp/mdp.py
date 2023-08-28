import copy


class MDP:

    def __init__(self) -> None:
        self._transition_model: dict[tuple[any, any, any], float] = {}
        self._rewards: dict[tuple[any, any, any], float] = {}
        self._actions: dict[any, list[any]] = {}
        self._states: set[any] = set()
        self._next_states: dict[tuple[any, any], set[any]] = {}
        self._goal_states: set[any] = set()
        self._initial_state: any = None

    def add_state(self, state: any, actions: list[any], is_goal: bool = False, is_initial_state: bool = False) -> None:
        self._states.add(state)
        self._actions[state] = actions
        self._initial_state = state if is_initial_state else self._initial_state
        if is_goal:
            self._goal_states.add(state)

    def set_initial_state(self, state: any) -> None:
        self._initial_state = state

    def add_transition_state(self, state: any,
                             action: any,
                             next_state: any,
                             probability: float = 1.0,
                             reward: float = 0.0) -> None:
        transition = (state, action, next_state)
        if transition in self._transition_model:
            self._transition_model[transition] = self._transition_model[transition] + probability
        else:
            self._transition_model[transition] = probability
        self._rewards[transition] = reward
        self._next_states.setdefault((state, action), set())
        self._next_states[(state, action)].add(next_state)

    def states(self) -> set[any]:
        return self._states

    def next_possible_states(self, state: any, action: any) -> set[any]:
        return self._next_states[(state, action)]

    def state_actions(self, state: any) -> list[any]:
        return self._actions[state]

    def transition_probability(self, transition: tuple[any, any, any]) -> float:
        return self._transition_model[transition]

    def transition_reward(self, transition: tuple[any, any, any]) -> float:
        return self._rewards[transition]


def value_iteration(mdp: MDP, t_max: int = 5, discount_factor: float = 1.0) -> dict[any, float]:
    expected_utility_by_state: dict[any, float] = {state: 0.0 for state in mdp.states()}

    for _ in range(0, t_max):
        expected_utility_by_state_copy = copy.deepcopy(expected_utility_by_state)
        for state in mdp.states():
            state_actions = mdp.state_actions(state)
            max_expected_utility = float('-inf')
            for action in state_actions:
                next_possible_states = mdp.next_possible_states(state, action)
                expected_utility = 0.0
                for next_state in next_possible_states:
                    expected_utility += mdp.transition_probability((state, action, next_state)) * \
                                        (mdp.transition_reward((state, action, next_state)) + discount_factor *
                                         expected_utility_by_state_copy[next_state])
                max_expected_utility = max(max_expected_utility, expected_utility)
            expected_utility_by_state[state] = max_expected_utility
    return expected_utility_by_state


if __name__ == '__main__':
    mdp = MDP()

    actions = ['UP', 'LEFT', 'RIGHT', 'DOWN']
    mdp.add_state((0, 0), actions)
    mdp.add_state((0, 1), actions)
    mdp.add_state((1, 0), actions)
    mdp.add_state((1, 1), actions)
    mdp.add_state((2, 0), actions)
    mdp.add_state((2, 1), actions)

    mdp.add_transition_state(state=(0, 0), action='UP', next_state=(0, 1), probability=0.8)
    mdp.add_transition_state(state=(0, 0), action='UP', next_state=(1, 0), probability=0.1)
    mdp.add_transition_state(state=(0, 0), action='UP', next_state=(0, 0), probability=0.1)
    mdp.add_transition_state(state=(0, 0), action='LEFT', next_state=(0, 0), probability=0.8)
    mdp.add_transition_state(state=(0, 0), action='LEFT', next_state=(0, 0), probability=0.1)
    mdp.add_transition_state(state=(0, 0), action='LEFT', next_state=(0, 1), probability=0.1)
    mdp.add_transition_state(state=(0, 0), action='RIGHT', next_state=(1, 0), probability=0.8)
    mdp.add_transition_state(state=(0, 0), action='RIGHT', next_state=(0, 1), probability=0.1)
    mdp.add_transition_state(state=(0, 0), action='RIGHT', next_state=(0, 0), probability=0.1)
    mdp.add_transition_state(state=(0, 0), action='DOWN', next_state=(0, 0), probability=0.8)
    mdp.add_transition_state(state=(0, 0), action='DOWN', next_state=(0, 0), probability=0.1)
    mdp.add_transition_state(state=(0, 0), action='DOWN', next_state=(1, 0), probability=0.1)

    mdp.add_transition_state(state=(1, 0), action='UP', next_state=(1, 1), probability=0.8, reward=10.0)
    mdp.add_transition_state(state=(1, 0), action='UP', next_state=(0, 0), probability=0.1, reward=10.0)
    mdp.add_transition_state(state=(1, 0), action='UP', next_state=(2, 0), probability=0.1, reward=10.0)
    mdp.add_transition_state(state=(1, 0), action='LEFT', next_state=(0, 0), probability=0.8, reward=10.0)
    mdp.add_transition_state(state=(1, 0), action='LEFT', next_state=(1, 0), probability=0.1)
    mdp.add_transition_state(state=(1, 0), action='LEFT', next_state=(1, 1), probability=0.1, reward=10.0)
    mdp.add_transition_state(state=(1, 0), action='RIGHT', next_state=(2, 0), probability=0.8, reward=10.0)
    mdp.add_transition_state(state=(1, 0), action='RIGHT', next_state=(1, 1), probability=0.1, reward=10.0)
    mdp.add_transition_state(state=(1, 0), action='RIGHT', next_state=(1, 0), probability=0.1)
    mdp.add_transition_state(state=(1, 0), action='DOWN', next_state=(1, 0), probability=0.8)
    mdp.add_transition_state(state=(1, 0), action='DOWN', next_state=(0, 0), probability=0.1, reward=10.0)
    mdp.add_transition_state(state=(1, 0), action='DOWN', next_state=(2, 0), probability=0.1, reward=10.0)

    mdp.add_transition_state(state=(2, 0), action='UP', next_state=(2, 1), probability=0.8)
    mdp.add_transition_state(state=(2, 0), action='UP', next_state=(1, 0), probability=0.1)
    mdp.add_transition_state(state=(2, 0), action='UP', next_state=(2, 0), probability=0.1)
    mdp.add_transition_state(state=(2, 0), action='LEFT', next_state=(1, 0), probability=0.8)
    mdp.add_transition_state(state=(2, 0), action='LEFT', next_state=(2, 1), probability=0.1)
    mdp.add_transition_state(state=(2, 0), action='LEFT', next_state=(2, 0), probability=0.1)
    mdp.add_transition_state(state=(2, 0), action='RIGHT', next_state=(2, 0), probability=0.8)
    mdp.add_transition_state(state=(2, 0), action='RIGHT', next_state=(2, 0), probability=0.1)
    mdp.add_transition_state(state=(2, 0), action='RIGHT', next_state=(2, 1), probability=0.1)
    mdp.add_transition_state(state=(2, 0), action='DOWN', next_state=(2, 0), probability=0.8)
    mdp.add_transition_state(state=(2, 0), action='DOWN', next_state=(2, 0), probability=0.1)
    mdp.add_transition_state(state=(2, 0), action='DOWN', next_state=(1, 0), probability=0.1)

    mdp.add_transition_state(state=(0, 1), action='UP', next_state=(0, 1), probability=0.8)
    mdp.add_transition_state(state=(0, 1), action='UP', next_state=(0, 1), probability=0.1)
    mdp.add_transition_state(state=(0, 1), action='UP', next_state=(1, 1), probability=0.1, reward=-100.0)
    mdp.add_transition_state(state=(0, 1), action='LEFT', next_state=(0, 1), probability=0.8)
    mdp.add_transition_state(state=(0, 1), action='LEFT', next_state=(0, 1), probability=0.1)
    mdp.add_transition_state(state=(0, 1), action='LEFT', next_state=(0, 0), probability=0.1, reward=-100.0)
    mdp.add_transition_state(state=(0, 1), action='RIGHT', next_state=(1, 1), probability=0.8, reward=-100.0)
    mdp.add_transition_state(state=(0, 1), action='RIGHT', next_state=(0, 0), probability=0.1, reward=-100.0)
    mdp.add_transition_state(state=(0, 1), action='RIGHT', next_state=(0, 1), probability=0.1)
    mdp.add_transition_state(state=(0, 1), action='DOWN', next_state=(0, 0), probability=0.8, reward=-100.0)
    mdp.add_transition_state(state=(0, 1), action='DOWN', next_state=(1, 1), probability=0.1, reward=-100.0)
    mdp.add_transition_state(state=(0, 1), action='DOWN', next_state=(0, 1), probability=0.1)

    mdp.add_transition_state(state=(1, 1), action='UP', next_state=(1, 1), probability=0.8)
    mdp.add_transition_state(state=(1, 1), action='UP', next_state=(0, 1), probability=0.1)
    mdp.add_transition_state(state=(1, 1), action='UP', next_state=(2, 1), probability=0.1)
    mdp.add_transition_state(state=(1, 1), action='LEFT', next_state=(0, 1), probability=0.8)
    mdp.add_transition_state(state=(1, 1), action='LEFT', next_state=(1, 0), probability=0.1)
    mdp.add_transition_state(state=(1, 1), action='LEFT', next_state=(1, 1), probability=0.1)
    mdp.add_transition_state(state=(1, 1), action='RIGHT', next_state=(2, 1), probability=0.8)
    mdp.add_transition_state(state=(1, 1), action='RIGHT', next_state=(1, 0), probability=0.1)
    mdp.add_transition_state(state=(1, 1), action='RIGHT', next_state=(1, 1), probability=0.1)
    mdp.add_transition_state(state=(1, 1), action='DOWN', next_state=(1, 0), probability=0.8)
    mdp.add_transition_state(state=(1, 1), action='DOWN', next_state=(0, 1), probability=0.1)
    mdp.add_transition_state(state=(1, 1), action='DOWN', next_state=(1, 0), probability=0.1)

    mdp.add_transition_state(state=(2, 1), action='UP', next_state=(2, 1), probability=0.8)
    mdp.add_transition_state(state=(2, 1), action='UP', next_state=(2, 1), probability=0.1)
    mdp.add_transition_state(state=(2, 1), action='UP', next_state=(1, 1), probability=0.1)
    mdp.add_transition_state(state=(2, 1), action='LEFT', next_state=(1, 1), probability=0.8)
    mdp.add_transition_state(state=(2, 1), action='LEFT', next_state=(2, 0), probability=0.1)
    mdp.add_transition_state(state=(2, 1), action='LEFT', next_state=(2, 1), probability=0.1)
    mdp.add_transition_state(state=(2, 1), action='RIGHT', next_state=(2, 1), probability=0.8)
    mdp.add_transition_state(state=(2, 1), action='RIGHT', next_state=(2, 1), probability=0.1)
    mdp.add_transition_state(state=(2, 1), action='RIGHT', next_state=(2, 0), probability=0.1)
    mdp.add_transition_state(state=(2, 1), action='DOWN', next_state=(2, 0), probability=0.8)
    mdp.add_transition_state(state=(2, 1), action='DOWN', next_state=(2, 1), probability=0.1)
    mdp.add_transition_state(state=(2, 1), action='DOWN', next_state=(1, 1), probability=0.1)

    print(value_iteration(mdp, t_max=2, discount_factor=0.9))
