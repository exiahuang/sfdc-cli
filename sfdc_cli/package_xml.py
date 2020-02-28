import os
from .setting import SfBasicConfig
from . import util, baseutil, logging
from .salesforce import (ToolingApi, MetadataApi)


class PackageXml():

    def __init__(self, project_dir=None):
        self.sf_basic_config = SfBasicConfig(project_dir)
        self.settings = self.sf_basic_config.get_setting()

    def buildFromDir(self,
                     scandir,
                     savepath,
                     filename="package.xml",
                     api_version="47.0"):
        migration_util = util.MigrationToolUtil(
            sf_basic_config=self.sf_basic_config, is_auto_download=False)
        migration_util.build_package_xml(
            os.path.join(savepath, filename),
            baseutil.SysIo().get_file_list(scandir), api_version)
        logging.info("%s" % os.path.join(savepath, filename))

    def buildFromServer(self, savepath, filename="package.xml"):
        meta_api = util.sf_login(self.sf_basic_config, Soap_Type=MetadataApi)
        packagexml = meta_api.buildPackageXml()
        baseutil.SysIo().save_file(full_path=os.path.join(savepath, filename),
                                   content=packagexml)
        logging.info("%s" % os.path.join(savepath, filename))
