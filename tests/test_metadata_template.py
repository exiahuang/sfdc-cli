import sys
from unittest import TestCase as PythonTestCase
from . import TEST_PROJECT_DIRECTORY
from sfdc_cli.metadata import Metadata


class MetadataTestCase(PythonTestCase):

    def test_metadata(self):
        print('*' * 80)
        print('run %s' % (sys._getframe().f_code.co_name))
        Metadata(TEST_PROJECT_DIRECTORY).new_apex("MyApexController",
                                                  "ApexClass.cls")
        Metadata(TEST_PROJECT_DIRECTORY).new_apex("MyApexControllerTest",
                                                  "UnitTestApexClass.cls")
        Metadata(TEST_PROJECT_DIRECTORY).new_apex("MyApexControllerTest2",
                                                  "UnitTestApexClass.cls")
        Metadata(TEST_PROJECT_DIRECTORY).new_apex("MyApexControllerBatch",
                                                  "BatchApexClass.cls")
        Metadata(TEST_PROJECT_DIRECTORY).new_trigger("MyApexTrigger", "Account",
                                                     "ApexTrigger.trigger")
        Metadata(TEST_PROJECT_DIRECTORY).new_page("MyApexVf", "ApexPage.page")
        Metadata(TEST_PROJECT_DIRECTORY).new_component("MyApexComponent")
        pass
