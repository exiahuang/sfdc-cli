import json
from .setting import SfBasicConfig
from . import util
from .salesforce import RestApi
import pprint


class SfRestApi():

    def __init__(self, project_dir=None):
        self.sf_basic_config = SfBasicConfig(project_dir)
        self.settings = self.sf_basic_config.get_setting()
        self.rest_api = util.sf_login(self.sf_basic_config, Soap_Type=RestApi)

    def call(self, endpoint, params=None, method='GET'):
        result = self.rest_api.call_rest(
            method=method,
            path=endpoint,
            params=params,
        )
        print(result.text)
