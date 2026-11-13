import unittest
from unittest.mock import patch

from main import get_positive_float


class TestGetPositiveFloat(unittest.TestCase):
    @patch("builtins.print")
    @patch("builtins.input", side_effect=["abc", "-5", "12.50"])
    def test_keeps_asking_until_valid(self, mock_input, mock_print):
        result = get_positive_float("Enter price: ")

        self.assertEqual(result, 12.50)
        self.assertEqual(mock_input.call_count, 3)
        printed = [call.args[0] for call in mock_print.call_args_list]
        self.assertEqual(printed, ["Please enter a valid number, e.g. 12.50",
                                   "Please enter a number greater than zero."])


if __name__ == "__main__":
    unittest.main()