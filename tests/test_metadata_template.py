import sys
from unittest import TestCase as PythonTestCase
from sfdc_cli.metadata import Metadata


class MetadataTestCase(PythonTestCase):

    def test_metadata(self):
        print('*' * 80)
        print('run %s' % (sys._getframe().f_code.co_name))
        Metadata().new_apex("MyApexController", "ApexClass.cls",
                            "temp/test-project/src", "47.0")
        Metadata().new_apex("MyApexControllerTest", "UnitTestApexClass.cls",
                            "temp/test-project/src", "47.0")
        Metadata().new_apex("MyApexControllerTest2", "UnitTestApexClass.cls",
                            "temp/test-project/src", "47.0")
        Metadata().new_apex("MyApexControllerBatch", "BatchApexClass.cls",
                            "temp/test-project/src", "47.0")
        Metadata().new_trigger("MyApexTrigger", "Account",
                               "ApexTrigger.trigger", "temp/test-project/src",
                               "47.0")
        Metadata().new_page("MyApexVf", "ApexPage.page",
                            "temp/test-project/src", "47.0")
        Metadata().new_component("MyApexComponent", "temp/test-project/src",
                                 "47.0")
        pass
