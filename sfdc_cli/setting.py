import os, time, json, re
from . import logging

AUTHENTICATION_OAUTH2 = "oauth2"
AUTHENTICATION_PASSWORD = "password"
config_dir = '.xyconfig'
sys_http_proxy = os.getenv('http_proxy', '')
sys_https_proxy = os.getenv('https_proxy', '')

OAUTH2_SETTING = {
    "client_id":
        "3MVG9YDQS5WtC11pNZnExZq_P8zQFHcFI0XKGSpyyMxC.GIuqp.5sOr37Hd0ZqCTGRNAImvRO16.P0Kxc2ZnK",
    "client_secret":
        "7230DB2DA454C7E4B04B7C3E3303B288CCB8336E46A8D627190D61FDB6D10331",
    "redirect_uri":
        "http://localhost:56888/auth/callback"
}


class SfBasicConfig():

    def __init__(self, project_dir=None):
        self._project_dir = project_dir
        self._load()
        self._init_proxy()

    def _load(self):
        # Load all settings
        self.setting = settings = {
            "workspace":
                self._project_dir,
            "project_dir":
                self._project_dir,
            "config_dir":
                os.path.join(self._project_dir, config_dir),
            "project_name":
                os.path.basename(self._project_dir),
            "project_config_path":
                os.path.join(self._project_dir, config_dir, "xyconfig.json"),
            "work_dir":
                os.path.join(self._project_dir, config_dir, "work")
        }

        settings["default_project"] = self.get_project_name()
        settings.update(self.get_project_config())
        session_config = self._get_session_config()
        if session_config:
            settings.update(session_config)

        settings["use_oauth2"] = (
            settings["authentication"] == AUTHENTICATION_OAUTH2)
        settings["use_password"] = (
            settings["authentication"] == AUTHENTICATION_PASSWORD)

        # set password default
        if not (settings["use_oauth2"] or settings["use_password"]):
            settings["use_password"] = True
            self.update_authentication_setting()

        if "is_sandbox" in settings:
            if settings["is_sandbox"]:
                settings["loginUrl"] = "https://test.salesforce.com"
            else:
                settings["loginUrl"] = "https://login.salesforce.com"

        return settings

    def _init_proxy(self):
        proxy = self.get_proxy()
        if proxy["use_proxy"]:
            http_proxy = sys_http_proxy
            if not http_proxy:
                if proxy["proxyuser"]:
                    http_proxy = "http://{user}:{password}@{server}".format(
                        user=proxy["proxyuser"],
                        password=proxy["proxypassword"],
                        server=proxy["proxyhost"])
                else:
                    http_proxy = "http://{server}".format(
                        server=proxy["proxyhost"])
                if proxy["proxyport"]:
                    http_proxy = http_proxy + ":" + proxy["proxyport"]
            os.environ["http_proxy"] = http_proxy
            os.environ["https_proxy"] = http_proxy
        else:
            if sys_http_proxy:
                os.environ["http_proxy"] = sys_http_proxy
            elif "http_proxy" in os.environ:
                os.environ.pop("http_proxy")

            if sys_https_proxy:
                os.environ["https_proxy"] = sys_https_proxy
            elif "https_proxy" in os.environ:
                os.environ.pop("https_proxy")
        logging.debug("http_proxy: %s" % os.getenv('http_proxy'))

    def save_session(self, session_str):
        logging.debug('session_str--->')
        logging.debug(session_str)
        full_path = os.path.join(self.get_project_dir(), config_dir, '.session')
        logging.debug('save .session path------->')
        logging.debug(full_path)
        logging.info('save session file, ' + full_path)
        content = json.dumps(session_str, indent=4)
        save_file(full_path, content)

    def get_default_browser(self):
        settings = self.setting
        default_browser = settings["default_browser"]
        browser_map = {}
        for browser in settings["browsers"]:
            broswer_path = settings["browsers"][browser]
            if os.path.exists(broswer_path):
                if default_browser == browser:
                    browser_map['name'] = browser
                    browser_map['path'] = broswer_path
                    return browser_map
                elif default_browser == "chrome-private" and browser == "chrome":
                    browser_map['name'] = "chrome-private"
                    browser_map['path'] = broswer_path
                    return browser_map

        browser_map['name'] = 'default'
        browser_map['path'] = ''
        return browser_map

    def get_browser_setting(self):
        dirs = []
        settings = self.setting
        default_browser = settings["default_browser"]

        for browser in settings["browsers"]:
            broswer_path = settings["browsers"][browser]
            if os.path.exists(broswer_path):
                dirs.append([browser, broswer_path])
        if settings["browsers"]["chrome"]:
            broswer_path = settings["browsers"]["chrome"]
            if os.path.exists(broswer_path):
                browser = "chrome-private"
                dirs.append([browser, broswer_path])
        # default browser
        if not dirs:
            dirs.append(["default", ""])
        return dirs

    def get_browser_setting2(self):
        dirs = []
        settings = self.setting
        default_browser = settings["default_browser"]

        for browser in settings["browsers"]:
            broswer_path = settings["browsers"][browser]
            if os.path.exists(broswer_path):
                if default_browser == browser:
                    browser_key = '[○]' + browser
                else:
                    browser_key = '[X]' + browser
                dirs.append([browser_key, browser])
        if settings["browsers"]["chrome"]:
            broswer_path = settings["browsers"]["chrome"]
            if os.path.exists(broswer_path):
                browser = "chrome-private"
                if default_browser == browser:
                    browser_key = '[○]' + browser
                else:
                    browser_key = '[X]' + browser
                dirs.append([browser_key, browser])
        # default browser
        if not dirs:
            dirs.append(["[○]default", "default"])
        return dirs

    def update_project_config(self, project_config):
        pro_config = self.get_project_config()
        pro_config.update(project_config)
        content = json.dumps(pro_config, indent=4)
        save_file(self.get_project_config_path(), content)

    def update_authentication_setting(self, auth_type=AUTHENTICATION_OAUTH2):
        logging.debug('>>>update_authentication_setting')
        pro_config = self.get_project_config()
        pro_config["authentication"] = auth_type
        content = json.dumps(pro_config, indent=4)
        save_file(self.get_project_config_path(), content)

    def update_default_browser(self, browser_name):
        logging.debug('>>>update_authentication_setting')
        pro_config = self.get_project_config()
        pro_config["default_browser"] = browser_name
        content = json.dumps(pro_config, indent=4)
        save_file(self.get_project_config_path(), content)

    def get_project_config(self):
        config_file_full_path = self.get_project_config_path()
        pro_config = None
        if os.path.isfile(config_file_full_path):
            # logging.debug('load project config : ' + config_file_full_path)
            with open(config_file_full_path) as fp:
                config_str = clear_comment(fp.read())
                pro_config = json.loads(config_str)
        else:
            return get_default_project_config(config_file_full_path,
                                              self.get_default_jar_home())
        return pro_config

    ###############
    def get_setting(self):
        return self.setting

    def get_project_dir(self):
        return self.setting["project_dir"]

    def get_work_dir(self):
        return self.setting["work_dir"]

    def get_tmp_dir(self):
        tmp_dir = os.path.join(self.get_config_dir(), ".tmp")
        if not os.path.exists(tmp_dir):
            os.makedirs(tmp_dir)
        return tmp_dir

    def get_ant_migration_tool_dir(self):
        return os.path.join(self.get_work_dir(), "MetadataBackupTools")

    def get_deploy_tmp_dir(self):
        return os.path.join(self.get_ant_migration_tool_dir(), "codepkg")

    def get_zip_dir(self):
        return os.path.join(self.setting["work_dir"], "zip")

    def get_test_dir(self):
        return os.path.join(self.setting["work_dir"], "test")

    def get_sfdc_module_dir(self):
        return os.path.join(self.setting["project_dir"], "src_sfdc_module")

    def get_config_dir(self):
        return self.setting["config_dir"]

    def get_project_name(self):
        return self.setting["project_name"]

    def get_project_config_path(self):
        return self.setting["project_config_path"]

    def is_use_os_terminal(self):
        return

    def get_proxy(self):
        if "proxy" in self.setting:
            return self.setting["proxy"]
        self.setting["proxy"] = {
            "use_proxy": False,
            "proxyhost": "127.0.0.1",
            "proxyport": "8888",
            "proxyuser": "proxyuser",
            "proxypassword": "proxypassword"
        }
        """
            "nonproxyhosts" : "",
            "socksproxyhost" : "",
            "socksproxyport" : ""
        """
        return self.setting["proxy"]

    def get_user_home_dir(self):
        home = os.path.expanduser("~")
        return os.path.join(home, "salesforce-project")

    def get_default_jar_home(self):
        if "jar_home" in self.setting:
            return self.setting["jar_home"]
        self.setting["jar_home"] = os.path.join(self.get_user_home_dir(), "jar")
        return self.setting["jar_home"]

    def get_auto_save_to_server(self):
        if "auto_save_to_server" in self.setting:
            return self.setting["auto_save_to_server"]
        self.setting["auto_save_to_server"] = False
        return self.setting["auto_save_to_server"]

    ###############private method
    # current project dir
    def _get_project_dir(self):
        if self._project_dir:
            return self._project_dir
        return '.'

    def _get_work_dir(self, xyfolder, is_auto_create=False):
        fullpath = os.path.join(self._get_project_dir(), xyfolder)
        # fix windows slash
        fullpath = os.path.normpath(fullpath)
        if is_auto_create:
            os.makedirs(fullpath)
        return fullpath

    def get_src_dir(self, sub_folder=""):
        return os.path.join(self.get_src_root(), self.setting["src_dir"],
                            sub_folder)

    def get_src_root(self):
        return self.setting["project_dir"]

    def get_winmerge(self):
        return self.get_app("winmerge")

    def get_apps(self):
        if "app" in self.setting:
            return self.setting["app"]
        return {}

    def get_app(self, app_type):
        if "app" in self.setting and app_type in self.setting["app"]:
            return self.setting["app"][app_type]
        return None

    def _get_session_config(self):
        config_file_full_path = os.path.join(self.get_project_dir(), config_dir,
                                             ".session")
        pro_config = None
        if os.path.isfile(config_file_full_path):
            logging.debug('load session : ' + config_file_full_path)
            with open(config_file_full_path) as fp:
                config_str = clear_comment(fp.read())
                pro_config = json.loads(config_str)
        return pro_config


def save_file(full_path, content, encoding='utf-8'):
    if not os.path.exists(os.path.dirname(full_path)):
        logging.debug("mkdir: " + os.path.dirname(full_path))
        os.makedirs(os.path.dirname(full_path))
    try:
        fp = open(full_path, "w", encoding=encoding)
        fp.write(content)
    except Exception as e:
        logging.error('save file error! ' + full_path)
        logging.error(e)
    finally:
        fp.close()


"""
    "loginUrl": "https://test.salesforce.com",
"""


def get_default_project_config(config_file_full_path, jar_home):
    if os.name == 'nt':
        jar_home = jar_home.replace("\\", "\\\\")

    pro_config = """{
    "username": "input your username",
    "password": "input your password",
    "security_token": "",
    "is_sandbox": true,
    "api_version": 47.0,
    "src_dir": "src",
    "authentication": "password", 
    "jar_home": "{jar_home}", 
    "debug_levels": {
        "Apex_Code": "DEBUG", 
        "Callout": "INFO", 
        "Workflow": "INFO", 
        "Apex_Profiling": "INFO", 
        "Validation": "INFO", 
        "DB": "Info", 
        "System": "DEBUG"
    },
    "proxy": {
        "use_proxy" : false,
        "proxyhost" : "127.0.0.1",
        "proxyport" : "8888",
        "proxyuser" : "proxyuser",
        "proxypassword" : "proxypassword"
    }
}
""".replace("{jar_home}",
            jar_home).replace("{winmerge}",
                              get_winmerge()).replace("{notepad}",
                                                      get_notepad())

    return json.loads(pro_config)


def get_winmerge():
    path1 = "C:\\Program Files (x86)\\WinMerge\\WinMergeU.exe"
    path2 = "C:\\Program Files\\WinMerge\\WinMergeU.exe"
    path = ""
    if os.path.exists(path1):
        path = path1
    elif os.path.exists(path2):
        path = path2
    return path.replace("\\", "\\\\")


def get_notepad():
    path1 = "C:\\Program Files (x86)\\Notepad++\\notepad++.exe"
    path2 = "C:\\Program Files\\Notepad++\\notepad++.exe"
    path = ""
    if os.path.exists(path1):
        path = path1
    elif os.path.exists(path2):
        path = path2
    return ("%s {file_name}" % path).replace("\\", "\\\\")


def clear_comment(src):
    # src = re.sub(r'((?<=\n)|^)[ \t]*\/\*.*?\*\/\n?|\/\*.*?\*\/|((?<=\n)|^)[ \t]*\/\/[^\n]*\n|\/\/[^\n]*', "", src)
    # logging.debug(src)
    return src
