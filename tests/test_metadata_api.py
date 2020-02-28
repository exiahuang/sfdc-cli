import sys
import json
from . import TEST_PROJECT_DIRECTORY
from unittest import TestCase as PythonTestCase
from sfdc_cli import baseutil
from sfdc_cli.metadata_api import MetadataApi
from sfdc_cli.retrieve import RetrieveApi


class FileAttrTestCase(PythonTestCase):

    def test_metadata(self):
        print('*' * 80)
        print('run %s' % (sys._getframe().f_code.co_name))
        attr = baseutil.SysIo().get_file_attr(
            TEST_PROJECT_DIRECTORY + "/src/classes/MyApexController.cls")
        print(json.dumps(attr, indent=2))
        attr = baseutil.SysIo().get_file_attr(
            TEST_PROJECT_DIRECTORY + "/src/aura/HelloWorld/HelloWorld.cmp")
        print(json.dumps(attr, indent=2))
        pass


class MetadataApiNewMetaTestCase(PythonTestCase):

    def test_metadata_new(self):
        print('*' * 80)
        print('run %s' % (sys._getframe().f_code.co_name))
        meta_api = MetadataApi(project_dir=TEST_PROJECT_DIRECTORY)
        print(json.dumps(meta_api.settings, indent=2))
        meta_api.new_metadata(TEST_PROJECT_DIRECTORY +
                              "/src/classes/MyApexController.cls")
        meta_api.new_metadata(TEST_PROJECT_DIRECTORY +
                              "/src/classes/MyApexControllerTest.cls")
        meta_api.new_metadata(TEST_PROJECT_DIRECTORY +
                              "/src/classes/MyApexControllerTest2.cls")
        meta_api.new_metadata(TEST_PROJECT_DIRECTORY +
                              "/src/classes/MyApexControllerBatch.cls")
        meta_api.new_metadata(TEST_PROJECT_DIRECTORY +
                              "/src/pages/MyApexVf.page")
        meta_api.new_metadata(
            TEST_PROJECT_DIRECTORY + "/src/triggers/MyApexTrigger.trigger",
            "Account")
        meta_api.new_metadata(TEST_PROJECT_DIRECTORY +
                              "/src/components/MyApexComponent.component")
        pass

    def test_metadata_cache(self):
        print('*' * 80)
        print('run %s' % (sys._getframe().f_code.co_name))
        meta_api = MetadataApi(project_dir=TEST_PROJECT_DIRECTORY)
        meta_api.reload_cache()
        pass


class MetadataApiAttrTestCase(PythonTestCase):

    def test_metadata_attr(self):
        print('*' * 80)
        print('run %s' % (sys._getframe().f_code.co_name))
        meta_api = MetadataApi(project_dir=TEST_PROJECT_DIRECTORY)
        meta_api.metadata_attr("ApexClass", 'classes/MyApexController.cls')
        pass


class MetadataApiDeleteTestCase(PythonTestCase):

    def test_metadata_delete(self):
        print('*' * 80)
        print('run %s' % (sys._getframe().f_code.co_name))
        meta_api = MetadataApi(project_dir=TEST_PROJECT_DIRECTORY)
        meta_api.delete_metadata(TEST_PROJECT_DIRECTORY +
                                 "/src/classes/MyApexController.cls")
        meta_api.delete_metadata(TEST_PROJECT_DIRECTORY +
                                 "/src/pages/MyApexVf.page")
        meta_api.delete_metadata(TEST_PROJECT_DIRECTORY +
                                 "/src/triggers/MyApexTrigger.trigger")
        meta_api.delete_metadata(TEST_PROJECT_DIRECTORY +
                                 "/src/components/MyApexComponent.component")
        pass

    def test_metadata_delete_arua(self):
        print('*' * 80)
        print('run %s' % (sys._getframe().f_code.co_name))
        meta_api = MetadataApi(project_dir=TEST_PROJECT_DIRECTORY)
        meta_api.delete_metadata(TEST_PROJECT_DIRECTORY +
                                 "/src/aura/HelloWorld")


class MetadataApiUpdateTestCase(PythonTestCase):

    def test_metadata_update(self):
        print('*' * 80)
        print('run %s' % (sys._getframe().f_code.co_name))
        meta_api = MetadataApi(project_dir=TEST_PROJECT_DIRECTORY)
        meta_api.update_metadata(filepath=TEST_PROJECT_DIRECTORY +
                                 "/src/classes/MyApexController.cls",
                                 isforce=False)
        pass

    def test_metadata_update_arua(self):
        print('*' * 80)
        print('run %s' % (sys._getframe().f_code.co_name))
        meta_api = MetadataApi(project_dir=TEST_PROJECT_DIRECTORY)
        meta_api.update_metadata(TEST_PROJECT_DIRECTORY +
                                 "/src/aura/HelloWorld/HelloWorld.cmp")


class MetadataApiRefreshTestCase(PythonTestCase):

    def test_metadata_refresh(self):
        print('*' * 80)
        print('run %s' % (sys._getframe().f_code.co_name))
        meta_api = MetadataApi(project_dir=TEST_PROJECT_DIRECTORY)
        meta_api.refresh_metadata(filepath=TEST_PROJECT_DIRECTORY +
                                  "/src/classes/MyApexController.cls")


class MetadataApiRefreshAuraTestCase(PythonTestCase):

    def test_metadata_refresh(self):
        print('*' * 80)
        print('run %s' % (sys._getframe().f_code.co_name))
        meta_api = MetadataApi(project_dir=TEST_PROJECT_DIRECTORY)
        meta_api.refresh_aura(aura_dir=TEST_PROJECT_DIRECTORY +
                              "/src/aura/HelloWorld")


class RetrieveApiTestCase(PythonTestCase):

    def test_describe(self):
        print('*' * 80)
        print('run %s' % (sys._getframe().f_code.co_name))
        desc = RetrieveApi(project_dir=TEST_PROJECT_DIRECTORY).describe()
        print(json.dumps(desc, indent=2))
        pass

    def test_retrieveAll(self):
        print('*' * 80)
        print('run %s' % (sys._getframe().f_code.co_name))
        RetrieveApi(project_dir=TEST_PROJECT_DIRECTORY).retrieve(
            savedir="temp", zipfilename="package.zip")
        pass

    def test_retrieve(self):
        print('*' * 80)
        print('run %s' % (sys._getframe().f_code.co_name))
        RetrieveApi(project_dir=TEST_PROJECT_DIRECTORY).retrieve(
            savedir="temp",
            zipfilename="package.zip",
            metaTypes=[
                "ApexClass", "ApexComponent", "ApexPage", "ApexTrigger",
                "ApexPage", "CustomObject", "AuraDefinitionBundle",
                "LightningComponentBundle"
            ])

    def test_unzip(self):
        print('*' * 80)
        print('run %s' % (sys._getframe().f_code.co_name))
        RetrieveApi(project_dir=TEST_PROJECT_DIRECTORY).unzip(
            zipfile="temp/package.zip",
            savedir="temp/test-unzip",
            srcpath="src")
        pass
