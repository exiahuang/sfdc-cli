import sys, os, shutil
from .setting import SfBasicConfig
from . import util, baseutil
from .salesforce import (SalesforceMoreThanOneRecord,
                         SalesforceMalformedRequest, SalesforceExpiredSession,
                         SalesforceRefusedRequest, SalesforceResourceNotFound,
                         SalesforceGeneralError, SalesforceError, ToolingApi,
                         MetadataApi)
from .const import AURA_DEFTYPE_EXT
from . import logging


class MetadataApi():

    def __init__(self, project_dir=None):
        self.sf_basic_config = SfBasicConfig(project_dir)
        self.settings = self.sf_basic_config.get_setting()
        self.meta_api = util.sf_login(self.sf_basic_config,
                                      Soap_Type=ToolingApi)
        self.metadata_util = util.MetadataUtil(self.sf_basic_config)

    def _print_success_message(self, meta_id, filepath):
        logging.info("local path : %s" % filepath)
        logging.info("sfdc url : https://%s/%s" %
                     (self.meta_api.sf_instance, meta_id))

    def new_metadata(self, filepath, object_name=None):
        try:
            attr = baseutil.SysIo().get_file_attr(filepath)
            metadata_type = attr['metadata_type']
            api_name = attr["name"]
            src_content = baseutil.read_file(filepath)
            if metadata_type == "ApexClass":
                status_code, result = self.meta_api.createApexClass(
                    api_name, src_content)
            elif metadata_type == "ApexTrigger":
                status_code, result = self.meta_api.createTrigger(
                    object_name, api_name, src_content)
            elif metadata_type == "ApexComponent":
                status_code, result = self.meta_api.createMetadata(
                    "ApexComponent", {
                        'MasterLabel': api_name,
                        'name': api_name,
                        'markup': src_content
                    })
            elif metadata_type == "ApexPage":
                status_code, result = self.meta_api.createMetadata(
                    "ApexPage", {
                        'MasterLabel': api_name,
                        'name': api_name,
                        'markup': src_content
                    })

            if status_code and status_code < 300 and status_code >= 200:
                logging.info("new %s done.  %s" % (metadata_type, result))
                if isinstance(result, dict) and 'id' in result:
                    self._print_success_message(result["id"], filepath)
            else:
                logging.info("new %s failed" % (metadata_type))
                logging.info("%s" % (result))
            logging.debug("new_metadata status_code %s" % (status_code))
            return status_code, result

        except Exception as ex:
            logging.error(ex)

    def metadata_attr(self, metadata_type, file_key):
        try:
            meta_dict = self.metadata_util.get_meta_by_category(metadata_type)
            return meta_dict.get(file_key, None)
        except Exception as ex:
            logging.error(ex)

    def delete_metadata(self, filepath, deletelocal=True, deletecache=True):
        try:
            meta_attr = self.metadata_util.get_meta_attr(filepath)
            status_code, result = self.meta_api.deleteMetadata(
                meta_attr["metadata_type"], meta_attr["id"])
            if deletelocal:
                if os.path.isdir(filepath):
                    shutil.rmtree(filepath)
                elif os.path.isfile(filepath):
                    os.remove(filepath)
            if deletecache:
                self.metadata_util.delete_metadata_cache(filepath)
            logging.info("delete file done! ")
            logging.debug("status_code: %s" % status_code)
            logging.debug("result: %s" % result)
        except Exception as ex:
            logging.error(ex)

    def reload_cache(self):
        try:
            logging.info('start to reload metadata cache')
            self.metadata_util.reload()
            logging.info('reload metadata cache done!')
        except Exception as ex:
            logging.error(ex)

    def update_metadata(self, filepath, isforce=False, deep=0):
        try:
            meta_attr = self.metadata_util.get_meta_attr(filepath)
            if not meta_attr or "id" not in meta_attr or not meta_attr["id"]:
                if deep < 1:
                    logging.info(
                        "metadata id not found, start to refresh cache...")
                    self.metadata_util.update_metadata_cache_by_filename(
                        filepath)
                    meta_attr = self.metadata_util.get_meta_attr(filepath)
                    deep = deep + 1
                    self.update_metadata(filepath, isforce, deep)
                    return
                logging.info("metadata id not found, please check it!")
                return
            logging.info(
                "start to update metadata : Id=%s, Name=%s, Type=%s." %
                (meta_attr["id"], meta_attr["file_name"], meta_attr["type"]))
            msg = self.metadata_util.is_modified(filepath, meta_attr["id"])
            if msg:
                if not isforce:
                    logging.info(msg)
                    return
            if meta_attr["is_lux"]:
                self._update_metadata_lux(filepath, meta_attr)
            else:
                self._update_meta_to_server(filepath, meta_attr)

        except Exception as ex:
            logging.error(ex)

    # Lightning update

    def _update_metadata_lux(self, filepath, meta_attr):
        body = baseutil.read_file(filepath)
        status_code, result = self.meta_api.updateLux(meta_attr["id"],
                                                      {"Source": body})
        if status_code > 300:
            logging.error("Lightning update error: %s" % result)
        else:
            self.metadata_util.update_metadata_cache(filepath, meta_attr["id"])
            self._print_success_message(meta_attr["id"], filepath)
            logging.info("update metadata done")

    # apex, visualforce, trigger, component update
    def _update_meta_to_server(self, filepath, meta_attr):
        body = baseutil.read_file(filepath)
        result = self.meta_api.updateMetadata(meta_attr["type"],
                                              meta_attr["id"], body)
        if not result["is_success"]:
            logging.error(result)
        else:
            self.metadata_util.update_metadata_cache(filepath, meta_attr["id"])
            self._print_success_message(meta_attr["id"], filepath)
            logging.info("update metadata done")

    def refresh_metadata(self, filepath, deep=0):
        meta_attr = self.metadata_util.get_meta_attr(filepath)
        if not meta_attr or "id" not in meta_attr or not meta_attr["id"]:
            if deep < 1:
                logging.info("metadata id not found, start to refresh cache...")
                self.metadata_util.update_metadata_cache_by_filename(filepath)
                meta_attr = self.metadata_util.get_meta_attr(filepath)
                deep = deep + 1
                self.refresh_metadata(filepath, deep)
                return
            logging.error("metadata id not found, please check it!")
            return
        logging.info("filepath: %s" % filepath)
        logging.info(
            "start to refresh metadata : Id=%s, Name=%s, Type=%s." %
            (meta_attr["id"], meta_attr["file_name"], meta_attr["type"]))
        try:
            status_code, result = self.meta_api.getMetadata(
                meta_attr["type"], meta_attr["id"])
            if status_code == 200:
                logging.info('refresh success')
                if meta_attr["type"] in ["ApexClass", "ApexTrigger"]:
                    content_key = "Body"
                elif meta_attr["type"] in ["ApexPage", "ApexComponent"]:
                    content_key = "Markup"
                elif meta_attr["type"] in ["AuraDefinition"]:
                    content_key = "Source"
                baseutil.SysIo().save_file(full_path=filepath,
                                           content=result[content_key])
                self.metadata_util.update_metadata_cache(
                    filepath, meta_attr["id"])
            else:
                logging.error('refresh error code ' + str(status_code))
                logging.error(result)
        except Exception as ex:
            logging.error(ex)

    def _check_is_aura_dir(self, targetdir):
        _targetdir = os.path.abspath(targetdir)
        aura_name = os.path.basename(_targetdir)
        dir_path = os.path.dirname(_targetdir)
        dir_name = os.path.basename(dir_path)
        return dir_name == "aura"

    def refresh_aura(self, aura_dir, deep=0):
        if not self._check_is_aura_dir(aura_dir):
            logging.error("It seems not a lightinig component! %s " % aura_dir)
            return
        if not os.path.exists(aura_dir):
            os.makedirs(aura_dir)
        attr = baseutil.SysIo().get_file_attr(aura_dir)
        aura_soql = "SELECT Id, CreatedDate, CreatedById, CreatedBy.Name, LastModifiedDate, LastModifiedById, LastModifiedBy.Name, AuraDefinitionBundle.DeveloperName, AuraDefinitionBundleId, DefType, Format, Source FROM AuraDefinition"
        aura_soql = aura_soql + " Where AuraDefinitionBundle.DeveloperName = '%s'" % (
            attr["file_name"])
        result = self.meta_api.query(aura_soql)
        if 'records' in result and len(result['records']) > 0:
            for file in os.listdir(aura_dir):
                if not "-meta.xml" in file:
                    os.remove(os.path.join(aura_dir, file))
            for AuraDefinition in result['records']:
                if AuraDefinition["DefType"] in AURA_DEFTYPE_EXT:
                    fileName = attr["file_name"] + AURA_DEFTYPE_EXT[
                        AuraDefinition["DefType"]]
                    baseutil.SysIo().save_file(full_path=os.path.join(
                        aura_dir, fileName),
                                               content=AuraDefinition["Source"])
            self.metadata_util.update_lux_metas(result['records'])
            logging.info("Refresh lightinig ok! ")
        else:
            logging.error("Refresh lightinig error! ")
