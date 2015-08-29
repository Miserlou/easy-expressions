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

    def test_easy_test(self):
        easy = Easy().startOfLine().exactly(1).of("p")
        self.assertTrue(easy.test('p'))
        self.assertFalse(easy.test('qp'))

    def test_match(self):
        easy = Easy().startOfLine().exactly(1).of("p")
        self.assertTrue(easy.match('q') is None)
        self.assertTrue(easy.match('p') is not None)

    def test_search(self):
        easy = Easy().startOfLine().exactly(1).of("p")
        self.assertTrue(easy.search('q') is None)
        self.assertTrue(easy.search('p') is not None)

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

    def test_exactly(self):
        """
        Test 'exactly'
        """
        reg = Easy() \
                .startOfLine() \
                .exactly(3).of("x") \
                .endOfLine() \
                .getRegex()

        test = "xx"
        self.assertTrue(len(re.findall(reg, test)) == 0)
        test = "xxx"
        self.assertTrue(len(re.findall(reg, test)) == 1)
        test = "xxxx"
        self.assertTrue(len(re.findall(reg, test)) == 0)

    def test_max(self):
        """
        Test 'max'
        """
        reg = Easy() \
                .startOfLine() \
                .max(3).of("x") \
                .endOfLine() \
                .getRegex()

        test = "xx"
        self.assertTrue(len(re.findall(reg, test)) == 1)
        test = "xxx"
        self.assertTrue(len(re.findall(reg, test)) == 1)
        test = "xxxx"
        self.assertTrue(len(re.findall(reg, test)) == 0)

    def test_min_max(self):
        """
        Test joined Min and Max
        """
        reg = Easy() \
                .startOfLine() \
                .min(3).max(5).of("x") \
                .endOfLine() \
                .getRegex()

        test = "xx"
        self.assertTrue(len(re.findall(reg, test)) == 0)
        test = "xxx"
        self.assertTrue(len(re.findall(reg, test)) == 1)
        test = "xxxx"
        self.assertTrue(len(re.findall(reg, test)) == 1)
        test = "xxxxx"
        self.assertTrue(len(re.findall(reg, test)) == 1)
        test = "xxxxxx"
        self.assertTrue(len(re.findall(reg, test)) == 0)

    def test_of(self):
        """
        Test of
        """
        easy = Easy() \
                .startOfLine() \
                .exactly(2).of("p p p ") \
                .endOfLine()

        test = "p p p p p p "
        self.assertTrue(easy.test(test))
        test = "p p p p pp"
        self.assertFalse(easy.test(test))

    def test_of_any(self):
        """
        Test ofAny
        """
        easy = Easy() \
                .startOfLine() \
                .exactly(3).ofAny() \
                .endOfLine()

        self.assertTrue(easy.test("abc"))
        self.assertFalse(easy.test("ac"))

    def test_groups(self):
        """
        Test asGroup and ofGroup
        """
        easy = Easy() \
                .startOfLine() \
                .exactly(3).of("p").asGroup() \
                .exactly(1).of("q") \
                .exactly(1).ofGroup(1) \
                .endOfLine()

        self.assertTrue(easy.test("pppqppp"))
        self.assertFalse(easy.test("pxpqppp"))

    def test_from(self):
        """
        Test asGroup and ofGroup
        """
        easy = Easy() \
                .startOfLine() \
                .exactly(3).of("p").asGroup() \
                .exactly(1).of("q") \
                .exactly(1).ofGroup(1) \
                .endOfLine()

        self.assertTrue(easy.test("pppqppp"))
        self.assertFalse(easy.test("pxpqppp"))

    # def test_endOfLine(self):

    #     one_p = Easy().exactly(1).of("p")
    #     regex = Easy().startOfLine().either(one_p).getRegex()#.orr(Easy().exactly(2).of("q")).getRegex();#.endOfLine().getRegex();

if __name__ == '__main__':
    unittest.main()
