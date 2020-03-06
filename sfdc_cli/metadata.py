#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from sfdc_cli.version import __version__
from .setting import SfBasicConfig
from .templates.template import Template
from . import baseutil, logging


class Metadata():

    def __init__(self, project_dir=None):
        self.sf_basic_config = SfBasicConfig(project_dir)
        self.settings = self.sf_basic_config.get_setting()

    def _new_metadata(self, metadata_type, template_name, api_name, object_name,
                      is_overwrite):
        api_version = self.settings["api_version"]
        src_dir = self.settings["src_dir"]
        data = {"api_name": api_name, "object_name": object_name}
        src = Template().get_src(metadata_type, template_name, data)
        attr = self.get_attr(metadata_type)
        save_path = os.path.join(src_dir, attr["folder"],
                                 "%s%s" % (api_name, attr["ext"]))
        relate_path = baseutil.get_slash().join(
            [src_dir, attr["folder"],
             "%s%s" % (api_name, attr["ext"])])
        if os.path.exists(save_path):
            if is_overwrite:
                logging.info("overwrite file")
            else:
                logging.info("file exist : %s " % (relate_path))
                return
        baseutil.SysIo().save_file(save_path, content=src)
        self._build_meta_xml(metadata_type, save_path, api_name, api_version)
        logging.info("init %s done: %s" % (metadata_type, relate_path))

    def get_attr(self, metadata_type):
        attr = {}
        if metadata_type == "ApexClass":
            attr = {"ext": ".cls", "folder": "classes"}
        elif metadata_type == "ApexTrigger":
            attr = {"ext": ".trigger", "folder": "triggers"}
        elif metadata_type == "ApexComponent":
            attr = {"ext": ".component", "folder": "components"}
        elif metadata_type == "ApexPage":
            attr = {"ext": ".page", "folder": "pages"}
        return attr

    def _build_meta_xml(self, metadata_type, full_path, api_name, api_version):
        if metadata_type in ["ApexClass", "ApexTrigger"]:
            meta_xml = "\n".join([
                "<?xml version=\"1.0\" encoding=\"UTF-8\"?>",
                "<{0} xmlns=\"http://soap.sforce.com/2006/04/metadata\">",
                "    <apiVersion>{1}</apiVersion>",
                "    <status>Active</status>", "</{0}>"
            ]).format(metadata_type, api_version)
        elif metadata_type in ["ApexPage", "ApexComponent"]:
            meta_xml = "\n".join([
                "<?xml version=\"1.0\" encoding=\"UTF-8\"?>",
                "<{0} xmlns=\"http://soap.sforce.com/2006/04/metadata\">",
                "    <apiVersion>{1}</apiVersion>", "    <label>{2}</label>",
                "</{0}>"
            ]).format(metadata_type, api_version, api_name)
        baseutil.SysIo().save_file(full_path=full_path + "-meta.xml",
                                   content=meta_xml)

    def new_apex(self, api_name, template_name, is_overwrite):
        self._new_metadata("ApexClass",
                           template_name,
                           api_name,
                           object_name="",
                           is_overwrite=is_overwrite)

    def new_page(self, api_name, template_name, is_overwrite):
        self._new_metadata("ApexPage",
                           template_name,
                           api_name,
                           object_name="",
                           is_overwrite=is_overwrite)

    def new_component(self, api_name, is_overwrite):
        self._new_metadata("ApexComponent",
                           template_name="ApexComponent.component",
                           api_name=api_name,
                           object_name="",
                           is_overwrite=is_overwrite)

    def new_trigger(self, api_name, object_name, template_name, is_overwrite):
        self._new_metadata("ApexTrigger",
                           template_name,
                           api_name,
                           object_name=object_name,
                           is_overwrite=is_overwrite)
