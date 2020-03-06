import sys, os, shutil
from .setting import SfBasicConfig
from . import util, baseutil
from .salesforce import (ToolingApi, MetadataApi)
from .const import AURA_DEFTYPE_EXT
from .templates import AntConfig


class AntTools():

    def __init__(self, project_dir=None):
        self.sf_basic_config = SfBasicConfig(project_dir)
        self.settings = self.sf_basic_config.get_setting()

    def _copy_build_xml(self, save_path, template_name):
        # not download ant-salesforce.jar
        migration_util = util.MigrationToolUtil(
            sf_basic_config=self.sf_basic_config)
        config_data = {
            "username": self.settings["username"],
            "password": self.settings["password"],
            "serverurl": self.settings["loginUrl"],
            "jar_path": migration_util.get_jar_path(),
            "jar_url_path": migration_util.get_jar_url_path(),
            "proxy": self.sf_basic_config.get_proxy()
        }
        ant_config = AntConfig()
        ant_config.build_migration_tools(save_path=save_path,
                                         config_data=config_data,
                                         template_name=template_name)

    def build_migration_tools(self, savedir):
        print('start to build migration tool')
        self._copy_build_xml(savedir, "MigrationTools")
        # meta_api = util.sf_login(self.sf_basic_config, Soap_Type=MetadataApi)
        # packagexml = meta_api.buildPackageXml()
        # baseutil.SysIo().save_file(full_path=os.path.join(
        #     savedir, "package.xml"),
        #                            content=packagexml)
        print('build migration tool success!')
