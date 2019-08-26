from .offer import Offer


class AtomicConstraint():
    def __init__(self, issue: str, value: str):
        self.issue = str(issue)
        self.value = str(value)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, AtomicConstraint):
            return False

        if self.issue != other.issue:
            return False

        if self.value != other.value:
            return False

        return True

    def is_satisfied_by_assignment(self, issue: str, value: str) -> bool:
        return not (issue == self.issue and value == self.value)

    def is_satisfied_by_offer(self, offer: Offer) -> bool:

        chosen_value = offer.get_chosen_value(self.issue)
        if chosen_value == self.value:
            return False
        else:
            return True

    # def is_satisfied_by_strat(self, strat: Strategy) -> bool:

    #     constrainted_prob = stratagy.get_prob(self.issue, self.value)
    #     return isclose(constrainted_prob, 0)

    def __hash__(self) -> int:
        return hash((self.issue, self.value))

    def __repr__(self) -> str:
        return "{issue}!={value}".format(issue=self.issue, value=self.value)