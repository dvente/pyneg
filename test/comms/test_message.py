import unittest

from pyneg.comms import Offer, AtomicConstraint, Message
from pyneg.types import MessageType


class TestMessage(unittest.TestCase):

    def setUp(self):
        self.generic_offer = Offer({"first": {"True": 1}, "second": {
            "False": 1}, "third": {"-3": 1}, "forth": {"1.8": 1}})
        self.empty_message = Message("A", "B", MessageType.EMPTY, None)
        self.accept_message = Message(
            "A", "B", MessageType.ACCEPT, self.generic_offer)
        self.termination_message = Message(
            "A", "B", MessageType.EXIT, None)
        self.constraint_message = Message(
            "A", "B", MessageType.OFFER, self.generic_offer, AtomicConstraint("dummy1", "True"))
        self.offer_message = Message(
            "A", "B", MessageType.OFFER, self.generic_offer)
        self.offer_string = "[first->True, second->False, third->-3, forth->1.8]"
        self.offer_message_string = "(A=>B;OFFER;{offer})".format(
            offer=self.offer_string)
        self.empty_message_string = "(A=>B;EMPTY)".format(
            offer=self.offer_string)
        self.accept_message_string = "(A=>B;ACCEPT;{})".format(
            self.offer_string)
        self.constraint_message_string = "(A=>B;OFFER;{offer};{constraint})".format(
            offer=self.offer_string,
            constraint=AtomicConstraint("dummy1", "True"))
        self.termination_message_string = "(A=>B;EXIT)"

    def tearDown(self):
        pass

    def test_empty_message_cant_have_content(self):
        with self.assertRaises(ValueError):
            Message("A", "B", MessageType.EMPTY, "content")  # type: ignore

    def test_invalid_message_kind_raises_value_error(self):
        with self.assertRaises(ValueError):
            Message("A", "B", "Unknown type", "random content")  # type: ignore

    def test_constraint_message_with_wrong_data_type_raises_value_error(self):
        with self.assertRaises(ValueError):
            Message("A", "B", MessageType.OFFER, "wrong data type")  # type: ignore

    def test_get_constraint_from_non_constraint_message_raises_error(self):
        with self.assertRaises(ValueError):
            self.empty_message.get_constraint()

    def test_get_offer(self):
        self.assertEqual(self.offer_message.offer, self.generic_offer)

    def test_get_constraint(self):
        self.assertEqual(self.constraint_message.get_constraint(),
                         AtomicConstraint("dummy1", "True"))

    def test_empty_message_is_empty(self):
        self.assertTrue(self.empty_message.is_empty())

    def test_empty_message_is_not_termination(self):
        self.assertFalse(self.empty_message.is_termination())

    def test_empty_message_is_not_offer(self):
        self.assertFalse(self.empty_message.is_offer())

    def test_empty_message_has_not_constraint(self):
        self.assertFalse(self.empty_message.has_constraint())

    def test_empty_message_is_not_acceptation(self):
        self.assertFalse(self.empty_message.is_acceptance())

    def test_acceptation_message_is_not_emtpy(self):
        self.assertFalse(self.accept_message.is_empty())

    def test_acceptation_message_is_not_termination(self):
        self.assertFalse(self.accept_message.is_termination())

    def test_acceptation_message_is_not_offer(self):
        self.assertFalse(self.accept_message.is_offer())

    def test_acceptation_message_is_acceptation(self):
        self.assertTrue(self.accept_message.is_acceptance())

    def test_termination_message_is_not_emtpy(self):
        self.assertFalse(self.termination_message.is_empty())

    def test_termination_message_is_termination(self):
        self.assertTrue(self.termination_message.is_termination())

    def test_termination_message_is_not_offer(self):
        self.assertFalse(self.termination_message.is_offer())

    def test_termination_message_is_not_acceptation(self):
        self.assertFalse(self.termination_message.is_acceptance())

    def test_constraint_message_is_not_emtpy(self):
        self.assertFalse(self.constraint_message.is_empty())

    def test_constraint_message_is_not_termination(self):
        self.assertFalse(self.constraint_message.is_termination())

    def test_constraint_message_has_constraint(self):
        self.assertTrue(self.constraint_message.has_constraint())

    def test_constraint_message_is_not_acceptation(self):
        self.assertFalse(self.constraint_message.is_acceptance())

    def test_offer_message_is_not_emtpy(self):
        self.assertFalse(self.offer_message.is_empty())

    def test_offer_message_is_not_termination(self):
        self.assertFalse(self.offer_message.is_termination())

    def test_offer_message_is_offer(self):
        self.assertTrue(self.offer_message.is_offer())

    def test_offer_message_is_not_acceptation(self):
        self.assertFalse(self.offer_message.is_acceptance())

    def test_eq_is_reflexive(self):
        self.assertTrue(self.offer_message == self.offer_message)

    def test_eq_is_symmetrical(self):
        a = self.offer_message
        b = self.offer_message
        self.assertTrue(a == b and b == a)

    def test_offer_message_formatting(self):
        self.assertEqual(self.offer_message_string, str(self.offer_message))

    def test_empty_message_formating(self):
        self.assertEqual(self.empty_message_string, str(self.empty_message))

    def test_accept_message_formating(self):
        self.assertEqual(self.accept_message_string,
                         str(self.accept_message))

    def test_termination_message_formatting(self):
        self.assertEqual(
            self.termination_message_string, str(self.termination_message))

    def test_constraint_message_formatting(self):
        self.assertEqual(
            self.constraint_message_string, str(self.constraint_message))

    def test_non_dict_offer_raises_error(self):
        with self.assertRaises(ValueError):
            Message("A", "B", MessageType.OFFER, Message(
                "A", "B", "offer", {"dummy1": {"True": 1}}))  # type: ignore

    def test_non_empty_message_without_offer_raises_error(self):
        with self.assertRaises(ValueError):
            Message("A", "B", MessageType.OFFER, None)
