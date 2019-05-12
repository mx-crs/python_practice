import unittest
from factorize import factorize


class TestFactorize(unittest.TestCase):
    def test_wrong_types_raise_exception(self):
        for case in 'string', 1.5:
            with self.subTest(x=case):
                self.assertRaises(TypeError, factorize, case)

    def test_negative(self):
        for case in -1, -10, -100:
            with self.subTest(x=case):
                self.assertRaises(ValueError, factorize, case)

    def test_zero_and_one_cases(self):
        for case in 0, 1:
            with self.subTest(x=case):
                self.assertEqual(factorize(case), (case,))

    def test_simple_numbers(self):
        for case in 3, 13, 29:
            with self.subTest(x=case):
                self.assertEqual(factorize(case), (case,))

    def test_two_simple_multipliers(self):
        cases = {
            6: (2, 3),
            26: (2, 13),
            121: (11, 11)
        }
        for case in cases:
            with self.subTest(x=case):
                self.assertEqual(factorize(case), cases[case])

    def test_many_multipliers(self):
        cases = {
            1001: (7, 11, 13),
            9699690: (2, 3, 5, 7, 11, 13, 17, 19)
        }
        for case in cases:
            with self.subTest(x=case):
                self.assertEqual(factorize(case), cases[case])

if __name__ == "__main__":
    unittest.main()