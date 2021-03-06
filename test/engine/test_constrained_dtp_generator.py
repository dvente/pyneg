from unittest import TestCase

from pyneg.comms import Offer, AtomicConstraint
from pyneg.engine import ConstrainedDTPGenerator, ConstrainedProblogEvaluator


class TestConstrainedDTPGenerator(TestCase):

    def setUp(self):
        self.neg_space = {
            "boolean": [True, False],
            "integer": list(range(10)),
            "float": [float("{0:.2f}".format(0.1 * i)) for i in range(10)]
        }
        self.utilities = {
            "boolean_True": 100,
            "boolean_False": 10,
            "integer_9": 100,
            "integer_3": 10,
            "integer_1": 0.1,
            "integer_4": -10,
            "integer_5": -100,
            "'float_0.1'": 1
        }

        self.kb = [
            "boolean_True :- integer_2, 'float_0.1'."
        ]

        # should have a utility of 100
        self.nested_test_offer = {
            "boolean": {"True": 1, "False": 0},
            "integer": {str(i): 0 for i in range(10)},
            "float": {"{0:.1f}".format(i * 0.1): 0 for i in range(10)}
        }
        self.nested_test_offer["integer"]["3"] = 1
        self.nested_test_offer['float']["0.6"] = 1
        self.nested_test_offer = Offer(self.nested_test_offer)

        self.optimal_offer = {
            "boolean": {"True": 1.0, "False": 0.0},
            "integer": {str(i): 0.0 for i in range(10)},
            "float": {"{0:.1f}".format(i * 0.1): 0.0 for i in range(10)}
        }
        self.optimal_offer["integer"]["9"] = 1.0
        self.optimal_offer['float']["0.1"] = 1.0
        self.optimal_offer = Offer(self.optimal_offer)
        self.max_util = 100 + 100 + 1
        self.constr_value = -2 * self.max_util

        self.violating_offer = {
            "boolean": {"True": 1.0, "False": 0.0},
            "integer": {str(i): 0.0 for i in range(10)},
            "float": {"{0:.1f}".format(i * 0.1): 0.0 for i in range(10)}
        }
        self.violating_offer["integer"]["2"] = 1.0
        self.violating_offer['float']["0.1"] = 1.0

        self.violating_offer = Offer(self.violating_offer)

        self.reservation_value = self.constr_value + 10
        self.non_agreement_cost = self.constr_value + 5

        self.generator = ConstrainedDTPGenerator(self.neg_space, self.utilities,
                                                 self.non_agreement_cost, self.reservation_value,
                                                 self.kb,
                                                 self.constr_value,
                                                 set())

    def test_responds_to_violating_offer_with_constraint(self):
        self.generator.add_constraint(AtomicConstraint("boolean", "True"))
        constr = self.generator.find_violated_constraint(self.violating_offer)
        self.assertTrue(constr in {AtomicConstraint(
            "boolean", "True"), AtomicConstraint("integer", "5")})

    def test_dtp_generates_optimal_bid_in_simple_negotiation_setting(self):
        result = self.generator.generate_offer()
        self.assertEqual(result, self.optimal_offer)

    # def test_doesnt_generate_same_offer_five_times(self):
    #     # since some elements might be randomly picked it can sometimes happen that the elements are the same but it
    #     # shouldn't keep happening so we'll try it a couple of times
    #     last_offer = self.generator.generate_offer()
    #     for i in range(20):
    #         new_offer = self.generator.generate_offer()
    #         self.assertNotEqual(last_offer, new_offer,i)
    #         last_offer = new_offer

    def test_generating_offer_records_it(self):
        _ = self.generator.generate_offer()
        self.assertTrue(Offer(
            {"'float_0.1'": 1.0, 'boolean_True': 1.0, 'boolean_False': 0.0, 'integer_1': 0.0, 'integer_3': 0.0,
             'integer_4': 0.0,
             'integer_5': 0.0, 'integer_9': 1.0}).get_sparse_repr() in self.generator.generated_offers.keys())

    def test_generates_valid_offers_when_constraints_are_present(self):
        arbitrary_utilities = {
            "boolean_True": 100,
            "boolean_False": 10,
            "integer_9": 100,
            "integer_3": 10,
            "integer_1": 0.1,
            "integer_4": -10,
            "integer_5": -100,
        }
        self.generator = ConstrainedDTPGenerator(
            self.neg_space,
            arbitrary_utilities,
            self.non_agreement_cost,
            self.reservation_value,
            self.kb, self.constr_value, set())

        # should not raise an exception
        offer = self.generator.generate_offer()
        self.assertEqual(self.neg_space.keys(), offer.get_issues())

    def test_ends_negotiation_if_offers_generated_are_not_acceptable(self):
        # simply a set of impossible utilities to check that we exit immediately
        self.arbitrary_utilities = {
            "boolean_True": 100,
            "boolean_False": 10,
            "integer_9": 100,
            "integer_3": 10,
            "integer_1": 0.1,
            "integer_4": -10,
            "integer_5": -100,
        }
        self.generator = ConstrainedDTPGenerator(
            self.neg_space,
            self.arbitrary_utilities,
            self.non_agreement_cost,
            500,
            self.kb, self.constr_value, set())

        with self.assertRaises(StopIteration):
            self.generator.generate_offer()

    def test_own_offer_does_not_violate_constraint(self):
        self.generator.add_constraint(AtomicConstraint("boolean", "True"))
        generated_offer = self.generator.generate_offer()
        self.assertTrue(
            self.generator.satisfies_all_constraints(generated_offer))

    def test_getting_utility_below_threshold_creates_constraint(self):
        low_util_dict = {"integer_4": -10000}
        self.generator.add_utilities(low_util_dict)
        self.assertTrue(AtomicConstraint("integer", "4")
                        in self.generator.constraints, self.generator.constraints)

    def test_all_values_can_get_constrained(self):
        low_util_dict = {"integer_{i}".format(
            i=i): -100000 for i in range(len(self.neg_space['integer']))}
        self.generator.add_utilities(low_util_dict)
        constraints = self.generator.constraints
        self.assertTrue(
            all([constr.issue == "integer" for constr in constraints]))
        self.assertEqual(
            len([constr.issue == "integer" for constr in constraints]),
            len(self.neg_space['integer']))

    def test_multiple_issues_can_get_constrained(self):
        low_util_dict = {"integer_4": -100000, "'float_0.9'": -100000}
        self.generator.add_utilities(low_util_dict)
        self.assertTrue({AtomicConstraint("integer", "4"), AtomicConstraint(
            "float", "0.9")}.issubset(self.generator.constraints))

    def test_terminates_after_constrains_become_unsatisfiable(self):
        self.generator.add_constraints({
            AtomicConstraint("boolean", "True"),
            AtomicConstraint("boolean", "False")})

        with self.assertRaises(StopIteration):
            _ = self.generator.generate_offer()

    def test_doesnt_create_unessecary_constraints_when_setting_multiple_utils(self):
        temp_issues = {
            "boolean1": ["True", "False"],
            "boolean2": ["True", "False"]
        }
        temp_utils = {
            "boolean1_True": -100000,
            "boolean1_False": 0,
            "boolean2_True": 10,
            "boolean2_False": 10
        }
        self.generator = ConstrainedDTPGenerator(temp_issues, temp_utils,
                                                 self.non_agreement_cost, self.reservation_value,
                                                 self.kb, self.constr_value, set())
        self.assertEqual(len(self.generator.constraints), 1)