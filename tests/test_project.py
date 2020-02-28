import sys
from . import TEST_PROJECT_ROOT, TEST_PROJECT_NAME
from unittest import TestCase as PythonTestCase
from sfdc_cli.project import Project


class ProjectTestCase(PythonTestCase):

    def test_init_project(self):
        print('*' * 80)
        print('run %s' % (sys._getframe().f_code.co_name))
        Project().init(root=TEST_PROJECT_ROOT, name=TEST_PROJECT_NAME)
        pass
