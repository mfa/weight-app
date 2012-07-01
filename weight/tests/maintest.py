#!/bin/env python
""" Part of weight_app

    :copyright: (c) 2012 by Andreas Madsack.
    :license: BSD, see LICENSE for more details.
"""

# testsuite
# run: python main.py

import unittest

import os
import sys

def suite():
    from base import BaseTest
    from test_importer import ImportTest
    from test_forms import FormTest

    suite = unittest.TestSuite()
    # Testmodules
    suite.addTest(unittest.makeSuite(BaseTest))
    suite.addTest(unittest.makeSuite(ImportTest))
    suite.addTest(unittest.makeSuite(FormTest))

    return suite


if __name__ == '__main__':
#    this_file=os.path.join(os.path.dirname(__file__),'../../env_weight/bin/activate_this.py')
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
    os.environ['TEST'] = 'yes'
    unittest.main(defaultTest='suite')
