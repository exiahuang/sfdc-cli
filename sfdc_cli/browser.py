from .setting import SfBasicConfig
from . import util
from .salesforce import (ToolingApi, MetadataApi)


class Browser():

    def __init__(self, project_dir=None):
        self.sf_basic_config = SfBasicConfig(project_dir)
        self.settings = self.sf_basic_config.get_setting()

    def open_src(self, filepath):
        metadata_util = util.MetadataUtil(self.sf_basic_config)
        meta_attr = metadata_util.get_meta_attr(filepath)
        metadata_util.open_in_web(meta_attr)

    def open_sobject(self, sobject):
        sobject_util = util.SobjectUtil(self.sf_basic_config)
        sobject_util.get_cache()
        sobject_util.open_in_web(sobject)

    def open_sobject(self, sobject):
        sobject_util = util.SobjectUtil(self.sf_basic_config)
        sobject_util.get_cache()
        sobject_util.open_in_web(sobject)

    def open_lightning_app(self, app_name):
        sf = util.sf_login(self.sf_basic_config)
        returl = '/c/' + app_name
        login_url = (
            'https://{instance}/secur/frontdoor.jsp?sid={sid}&retURL={returl}'.
            format(instance=sf.sf_instance, sid=sf.session_id, returl=returl))
        util.open_in_default_browser(self.sf_basic_config, login_url)

    def open_vf_page(self, vf_name):
        sf = util.sf_login(self.sf_basic_config)
        returl = '/apex/' + vf_name
        login_url = (
            'https://{instance}/secur/frontdoor.jsp?sid={sid}&retURL={returl}'.
            format(instance=sf.sf_instance, sid=sf.session_id, returl=returl))
        util.open_in_default_browser(self.sf_basic_config, login_url)
