import json
from .setting import SfBasicConfig
from . import util
from .salesforce import MetadataApi


class FolderApi():

    def __init__(self, project_dir=None):
        self.sf_basic_config = SfBasicConfig(project_dir)
        self.settings = self.sf_basic_config.get_setting()
        self.meta_api = util.sf_login(self.sf_basic_config,
                                      Soap_Type=MetadataApi)

    def list(self, name):
        print(
            json.dumps(self.meta_api.listFolder(name),
                       indent=4,
                       ensure_ascii=False))
