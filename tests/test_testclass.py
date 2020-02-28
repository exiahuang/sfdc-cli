import sys
import json
from . import TEST_PROJECT_DIRECTORY
from unittest import TestCase as PythonTestCase
from sfdc_cli.testclass import Testclass


class TestclassTestCase(PythonTestCase):

    def test_run_test(self):
        print('*' * 80)
        print('run %s' % (sys._getframe().f_code.co_name))
        Testclass(project_dir=TEST_PROJECT_DIRECTORY).run(
            TEST_PROJECT_DIRECTORY + "/src/classes/MyApexControllerTest.cls")
        pass

    def test_retrieve_apex_coverage(self):
        print('*' * 80)
        print('run %s' % (sys._getframe().f_code.co_name))
        Testclass(project_dir=TEST_PROJECT_DIRECTORY).retrieve_apex_coverage(
            savefile=TEST_PROJECT_DIRECTORY + "/log/apex_coverage.log")
        pass
