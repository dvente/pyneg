from pyneg.comms import Offer, AtomicConstraint
from pyneg.types import AtomicDict
from pyneg.engine.evaluator import Evaluator
from pyneg.engine.generator import Generator
from typing import Set, Optional

"""
this is the engine docstring
"""

class AbstractEngine:
    """The abstract engine is an empty stub. It has to purposes: 
    The first is to enable """
    def __init__(self):
        pass

    def generate_offer(self) -> Offer:
        raise NotImplementedError()

    def calc_offer_utility(self, offer: Offer) -> float:
        raise NotImplementedError()

    def add_utilities(self, new_utils: AtomicDict) -> bool:
        raise NotImplementedError()

    def set_utilities(self, new_utils: AtomicDict) -> bool:
        raise NotImplementedError()

    def add_constraint(self, constraint: AtomicConstraint) -> bool:
        raise NotImplementedError()

    def add_constraints(self, new_constraints: Set[AtomicConstraint]) -> bool:
        raise NotImplementedError()

    def find_violated_constraint(self, offer: Offer) -> Optional[AtomicConstraint]:
        raise NotImplementedError()

    def get_unconstrained_values_by_issue(self, issue):
        raise NotImplementedError()

    def get_constraints(self) -> Set[AtomicConstraint]:
        raise NotImplementedError()

    def accepts(self, offer: Offer) -> bool:
        raise NotImplementedError()

    def can_continue(self) -> bool:
        raise NotImplementedError()

    def satisfies_all_constraints(self,offer: Offer) -> bool:
        raise NotImplementedError()


class Engine(AbstractEngine):
    """Engine docstring"""
    def __init__(self, generator: Generator, evaluator: Evaluator):
        super().__init__()
        self.generator: Generator = generator
        self.evaluator: Evaluator = evaluator
        self._accepts_all = False

    def generate_offer(self) -> Offer:
        return self.generator.generate_offer()

    def calc_offer_utility(self, offer: Offer) -> float:
        return self.evaluator.calc_offer_utility(offer)

    def add_utilities(self, new_utils: AtomicDict) -> bool:
        self.evaluator.add_utilities(new_utils)
        return self.generator.add_utilities(new_utils)

    def set_utilities(self, new_utils: AtomicDict) -> bool:
        self.evaluator.add_utilities(new_utils)
        return self.generator.add_utilities(new_utils)

    def add_constraint(self, constraint: AtomicConstraint) -> bool:
        return self.generator.add_constraint(constraint)

    def add_constraints(self, new_constraints: Set[AtomicConstraint]) -> bool:
        return self.generator.add_constraints(new_constraints)

    def find_violated_constraint(self, offer: Offer) -> Optional[AtomicConstraint]:
        return self.generator.find_violated_constraint(offer)

    def get_unconstrained_values_by_issue(self, issue: str) -> Set[str]:
        return self.generator.get_unconstrained_values_by_issue(issue)

    def get_constraints(self) -> Set[AtomicConstraint]:
        return self.generator.get_constraints()

    def satisfies_all_constraints(self, offer: Offer) -> bool:
        for constr in self.generator.get_constraints():
            if not constr.is_satisfied_by_offer(offer):
                return False

        return True

    def accepts(self, offer: Offer) -> bool:
        if self._accepts_all:
            return True

        return self.evaluator.calc_offer_utility(offer) >= self.generator.acceptability_threshold

    def can_continue(self) -> bool:
        return self.generator.active