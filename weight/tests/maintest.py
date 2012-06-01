#!/bin/env python

# testsuite
# run: python main.py

import unittest

import os
import sys

def suite():
    from base import BaseTest

    suite = unittest.TestSuite()
    # Testmodules
    suite.addTest(unittest.makeSuite(BaseTest))

    return suite


if __name__ == '__main__':
#    this_file=os.path.join(os.path.dirname(__file__),'../../env_weight/bin/activate_this.py')
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
    os.environ['TEST'] = 'yes'
    unittest.main(defaultTest='suite')