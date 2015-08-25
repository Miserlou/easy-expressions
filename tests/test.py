import re
import string
import sys
import unittest
import logging

import nose
from nose import case
from nose.pyversion import unbound_method
from nose import util

from easy_expressions import Easy

class TestEasy(unittest.TestCase):

    def test_test(self):
        self.assertTrue(True)

    def empty_assert(self, assertme):
        self.assertNotEqual(assertme, '')
        self.assertNotEqual(assertme, None)

    def test_startOfLine(self):
        """
        Start of Line test.
        """

        reg = Easy().startOfLine().exactly(1).of("p").getRegex()

        test = "p"
        self.assertTrue(len(re.findall(reg, test)) == 1)

        test = "qp"
        self.assertTrue(len(re.findall(reg, test)) == 0)

    def test_dollars_example(self):
        """
        The first example from the README.
        """

        reg = Easy() \
                .find("$") \
                .min(1) \
                .digits() \
                .then(".") \
                .digit() \
                .digit() \
                .getRegex()

        test = "$10.00"
        self.assertTrue(len(re.findall(reg, test)) == 1)

        test = "$1X.00"
        self.assertFalse(len(re.findall(reg, test)) == 1)

    # def test_endOfLine(self):

    #     one_p = Easy().exactly(1).of("p")
    #     regex = Easy().startOfLine().either(one_p).getRegex()#.orr(Easy().exactly(2).of("q")).getRegex();#.endOfLine().getRegex();

if __name__ == '__main__':
    unittest.main()