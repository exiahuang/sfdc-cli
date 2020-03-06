import sys, os
from .setting import SfBasicConfig
from . import util, baseutil
from .salesforce import (ToolingApi, MetadataApi)
from . import logging


class DataApi():

    def __init__(self, project_dir=None):
        self.sf_basic_config = SfBasicConfig(project_dir)
        self.settings = self.sf_basic_config.get_setting()

    def soql_format(self, sf_instance, soql_str):
        import re
        soql = baseutil.del_comment(soql_str)
        match = re.match("select\s+\*\s+from[\s\t]+(\w+)([\t\s\S]*)", soql,
                         re.I | re.M)
        if match:
            sobject = match.group(1)
            condition = match.group(2)
            fields = self.get_sobject_fields(sf_instance, sobject)
            fields_str = ','.join(fields)
            soql = ("select %s from %s %s" % (fields_str, sobject, condition))

        return soql

    # get all fields from sobject
    def get_sobject_fields(self, sf_instance, sobject):
        fields = []
        sftype = sf_instance.get_sobject(sobject)
        sftypedesc = sftype.describe()
        for field in sftypedesc["fields"]:
            fields.append(baseutil.xstr(field["name"]))
        return fields

    def query(self, soql):
        try:
            sf = util.sf_login(self.sf_basic_config)
            soql_str = self.soql_format(sf, soql)
            logging.debug(soql_str)
            soql_result = sf.query(soql_str)
            message = baseutil.get_soql_result(soql_str, soql_result)
            print(message)
        except Exception as e:
            logging.error(e)
            return

    def query_tooling(self, soql):
        try:
            sf = util.sf_login(self.sf_basic_config)
            params = {'q': soql}
            soql_result = sf.restful('tooling/query', params)
            message = baseutil.get_soql_result(soql, soql_result)
            print(message)
        except Exception as e:
            logging.error(e)
            return
