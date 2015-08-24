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

        reg = Easy().startOfLine().exactly(1).of("p").getRegex()

        test = "p"
        self.assertTrue(len(re.findall(reg, test)) == 1)

        test = "qp"
        self.assertTrue(len(re.findall(reg, test)) == 0)

if __name__ == '__main__':
    unittest.main()