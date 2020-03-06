import os, shutil
from datetime import datetime
from .setting import SfBasicConfig
from . import util, baseutil
from .salesforce import (SalesforceMoreThanOneRecord,
                         SalesforceMalformedRequest, SalesforceExpiredSession,
                         SalesforceRefusedRequest, SalesforceResourceNotFound,
                         SalesforceGeneralError, SalesforceError, ToolingApi,
                         MetadataApi)
from .const import SF_FLODER_TO_TYPE
from . import logging


class RetrieveApi():

    def __init__(self, project_dir=None):
        self.sf_basic_config = SfBasicConfig(project_dir)
        self.project_dir = project_dir
        self.settings = self.sf_basic_config.get_setting()
        self.meta_api = util.sf_login(self.sf_basic_config,
                                      Soap_Type=MetadataApi)

    def describe(self):
        describeMetadataResult = self.meta_api.describeMetadata()
        return describeMetadataResult.get("metadataObjects", None)

    def retrieve(self, savedir, zipfilename, metaTypes=None):
        try:
            if metaTypes:
                retrive_metadata_desc = [
                    desc for desc in self.describe()
                    if desc["xmlName"] in metaTypes
                ]
                self.meta_api.retrieveZip(
                    save_dir=savedir,
                    zip_file_name=zipfilename,
                    retrive_metadata_objects=retrive_metadata_desc)
            else:
                self.meta_api.retrieveZip(save_dir=savedir,
                                          zip_file_name=zipfilename)
        except Exception as e:
            logging.error(e)
            return

    def refresh(self, dirs):
        sel_dirs = []
        for a_dir in dirs:
            dir_name = os.path.basename(a_dir)
            sel_dirs.append(dir_name)
            if dir_name not in SF_FLODER_TO_TYPE:
                logging.error("Not support type : %s ." % (dir_name))
                return

        retrive_metadata_objects = []
        for metaObj in self.meta_api.describeMetadata()["metadataObjects"]:
            if metaObj['directoryName'] in sel_dirs:
                retrive_metadata_objects.append(metaObj)
        if len(retrive_metadata_objects) > 0:
            tmp_dir = self.sf_basic_config.get_tmp_dir()
            tmp_file = os.path.join(tmp_dir, "tmp_src.zip")
            tmp_src_dir = os.path.join(tmp_dir, "tmp_src")
            if os.path.exists(tmp_file):
                os.remove(tmp_file)
            if os.path.exists(tmp_src_dir):
                shutil.rmtree(tmp_src_dir)
            self.meta_api.retrieveZip(
                zip_file_name=tmp_file,
                retrive_metadata_objects=retrive_metadata_objects)
            if os.path.exists(tmp_file):
                self.meta_api.unzipfile(tmp_file, tmp_src_dir,
                                        self.settings["src_dir"])
                tmp_package_xml_path = os.path.join(tmp_src_dir,
                                                    self.settings["src_dir"],
                                                    "package.xml")
                if os.path.exists(tmp_package_xml_path):
                    os.remove(tmp_package_xml_path)
                from distutils import dir_util
                dir_util.copy_tree(
                    os.path.join(tmp_src_dir, self.settings["src_dir"]),
                    os.path.join(self.sf_basic_config.get_src_root(),
                                 self.settings["src_dir"]))
        else:
            logging.error("refresh failed. ")

    def unzip(self, filepath, savedir, is_remove_zip):
        if os.path.exists(filepath):
            import zipfile
            from distutils import dir_util
            src_path = os.path.join(savedir, self.settings["src_dir"])
            base_src_dir = os.path.dirname(src_path)
            base_src_name = os.path.basename(src_path)
            unpackaged_path = os.path.join(base_src_dir, "unpackaged")
            with zipfile.ZipFile(filepath, 'r') as zf:
                zf.extractall(base_src_dir)

            if os.path.exists(src_path):
                dir_util.copy_tree(unpackaged_path, src_path)
                shutil.rmtree(unpackaged_path)
            else:
                shutil.move(unpackaged_path, src_path)

            if is_remove_zip:
                os.remove(filepath)
        else:
            logging.error("file not found, %s" % filepath)
