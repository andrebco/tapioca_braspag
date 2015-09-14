# coding: utf-8

import unittest

from tapioca_braspag import Braspag


class TestTapiocaBraspag(unittest.TestCase):

    def setUp(self):
        self.wrapper = Braspag()


if __name__ == '__main__':
    unittest.main()
