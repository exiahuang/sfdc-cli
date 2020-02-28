import os, shutil
from .setting import SfBasicConfig
from . import util, baseutil, logging


class Testclass():

    def __init__(self, project_dir=None):
        self.sf_basic_config = SfBasicConfig(project_dir)
        self.settings = self.sf_basic_config.get_setting()
        self.metadata_util = util.MetadataUtil(self.sf_basic_config)

    def run(self, filepath):
        self.metadata_util.run_test(
            [self.metadata_util.get_meta_attr(filepath).get("id")])

    def retrieve_apex_coverage(self, savefile):
        apex_coverage = "\n".join(self.metadata_util.get_apex_coverage())
        baseutil.SysIo().save_file(full_path=savefile, content=apex_coverage)
        logging.info(savefile)
