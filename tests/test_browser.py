import sys
from . import TEST_PROJECT_DIRECTORY
from unittest import TestCase as PythonTestCase
from sfdc_cli.browser import Browser


class BrowserTestCase(PythonTestCase):

    def test_open_src(self):
        print('*' * 80)
        print('run %s' % (sys._getframe().f_code.co_name))
        Browser(TEST_PROJECT_DIRECTORY).open_src(
            TEST_PROJECT_DIRECTORY + "/src/classes/MyApexController.cls")
        pass

    def test_open_aura(self):
        print('*' * 80)
        print('run %s' % (sys._getframe().f_code.co_name))
        Browser(TEST_PROJECT_DIRECTORY).open_src(
            TEST_PROJECT_DIRECTORY + "/src/aura/HelloWorld/HelloWorld.cmp")
        pass

    def test_open_account_sobject(self):
        print('*' * 80)
        print('run %s' % (sys._getframe().f_code.co_name))
        Browser(TEST_PROJECT_DIRECTORY).open_sobject("Account")
        pass

    def test_open_opp_sobject(self):
        print('*' * 80)
        print('run %s' % (sys._getframe().f_code.co_name))
        Browser(TEST_PROJECT_DIRECTORY).open_sobject("Opportunity")
        pass
