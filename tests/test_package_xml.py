import sys
from unittest import TestCase as PythonTestCase
from sfdc_cli import baseutil
from sfdc_cli.package_xml import PackageXml
import json

TEST_PROJECT_DIRECTORY = "temp/test-project"


class PackageXmlTestCase(PythonTestCase):

    def test_package_xml_from_server(self):
        print('*' * 80)
        print('run %s' % (sys._getframe().f_code.co_name))
        PackageXml(project_dir=TEST_PROJECT_DIRECTORY).buildFromServer(
            savepath="temp/packagexml", filename="package.xml")
        pass

    def test_package_xml_from_dir(self):
        print('*' * 80)
        print('run %s' % (sys._getframe().f_code.co_name))
        PackageXml(project_dir=TEST_PROJECT_DIRECTORY).buildFromDir(
            scandir="temp/test-project/",
            savepath="temp/packagexml-from-directory",
            filename="package.xml",
            api_version="47.0")
        pass
