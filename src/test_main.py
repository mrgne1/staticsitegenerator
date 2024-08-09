import unittest
import main

class TestExtractTitle(unittest.TestCase):

    def test_simple_title(self):
        title = main.extract_title("# header")
        expected = "header"

        self.assertEqual(expected, title)

    def test_leading_whitespace(self):
        title = main.extract_title("\n   # header")
        expected = "header"

        self.assertEqual(expected, title)

    def test_trailing_whitespace(self):
        title = main.extract_title("# header  \n\n")
        expected = "header"

        self.assertEqual(expected, title)

    def test_tolkien_fan_club(self):
        title = main.extract_title("# Tolkien Fan Club\n")
        expected = "Tolkien Fan Club"

        self.assertEqual(expected, title)


if __name__ == "__main__":
    unittest.main()