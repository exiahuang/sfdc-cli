import json
from . import util, baseutil
from .setting import SfBasicConfig
from . import logging


class Tools():

    def __init__(self):
        pass

    def copy_lightning(self, from_dir, to_dir):
        baseutil.SysIo().copy_lightning(from_dir, to_dir)

    def json_format(self, data):
        print(json.dumps(json.loads(data), indent=4, ensure_ascii=False))
