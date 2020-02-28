import os
import json
from datetime import datetime
from .baseutil import SysIo
from .setting import SfBasicConfig
from . import logging


class Project():

    def init(self, project_dir, init_sublime_projcet=False):
        logging.info("init project: %s" % project_dir)
        name = os.path.basename(project_dir)
        sf_basic_config = SfBasicConfig(project_dir=project_dir)
        # project_config = sf_basic_config.get_project_config()
        sf_basic_config.update_project_config({})
        logging.info('please modify config: ' +
                     sf_basic_config.get_project_config_path())
        if init_sublime_projcet:
            sublime_settings_path = os.path.join(project_dir,
                                                 name + ".sublime-project")
            if not os.path.exists(sublime_settings_path):
                self._mk_project_file(project_dir, sublime_settings_path)
            logging.debug("new sublime project done: %s" %
                          sublime_settings_path)

    def _mk_project_file(self, project_path, file_path):
        sysio = SysIo()
        logging.debug("make project file")
        sublime_settings = {
            "folders": [{
                "file_exclude_patterns": ["*.*-meta.xml"],
                "folder_exclude_patterns": [
                    self.sf_basic_config.get_xyfolder() + "/.tmp",
                    self.sf_basic_config.get_xyfolder() +
                    "/MetadataBackupTools/codepkg"
                ],
                "path": project_path
            }]
        }
        sysio.save_file(file_path, json.dumps(sublime_settings, indent=4))
