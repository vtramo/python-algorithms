from abc import ABCMeta, abstractmethod
from csp.csp_components import CSP, Variable
from csp.ac_3 import ac_3


class Inference(metaclass=ABCMeta):

    @abstractmethod
    def __call__(self, csp: CSP[Variable[any]], var: Variable[any], assignment: dict[Variable[any], any]) -> bool:
        pass


class ArcConsistencyInference(Inference):

    def __call__(self, csp: CSP[Variable[any]], var: Variable[any], assignment: dict[Variable[any], any]) -> bool:
        return ac_3(csp)
