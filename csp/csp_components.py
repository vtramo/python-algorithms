import uuid
from dataclasses import dataclass, field
from typing import TypeVar, Generic, Callable
from uuid import uuid4

D = TypeVar("D")


@dataclass(slots=True)
class Variable(Generic[D]):
    domain: list[D]
    unary_constraints: list[Callable[[D], bool]] = field(default_factory=lambda: [])
    id: str = ''

    def __post_init__(self):
        self.id = uuid4()

    def __hash__(self):
        return self.id.__hash__()

