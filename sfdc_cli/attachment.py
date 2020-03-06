import sys, os, shutil
from .setting import SfBasicConfig
from . import util, baseutil
from .salesforce import RestApi


class AttachmentApi():

    def __init__(self, project_dir=None):
        self.sf_basic_config = SfBasicConfig(project_dir)
        self.settings = self.sf_basic_config.get_setting()

    def download(self,
                 savedir,
                 limit=2000,
                 filename="{Id}_{Title}_v{VersionNumber}.{FileExtension}"):
        sf = util.sf_login(self.sf_basic_config, Soap_Type=RestApi)
        attachments = sf.query(
            "SELECT Id, Title, VersionNumber, FileExtension FROM ContentVersion LIMIT {limit}"
            .format(limit=limit))
        print("添付ファイル件数 : " + str(len(attachments["records"])))

        if not os.path.exists(savedir):
            os.makedirs(savedir)

        for attachment in attachments["records"]:
            print("start to download : %s, %s.%s" %
                  (attachment["Id"], attachment["Title"],
                   attachment["FileExtension"]))
            """
            Run Rest API : download attachment
            """
            rest_path = "/services/data/v{api_version}/sobjects/ContentVersion/{id}/VersionData".format(
                api_version=self.settings["api_version"], id=attachment["Id"])
            result = sf.call_rest(
                method='GET',
                path=rest_path,
                params={},
            )
            save_file_name = filename.replace("{Id}", attachment["Id"]).replace(
                "{Title}", attachment["Title"]).replace(
                    "{VersionNumber}", attachment["VersionNumber"]).replace(
                        "{FileExtension}", attachment["FileExtension"])
            with open(os.path.join(savedir, save_file_name), mode='wb') as f:
                f.write(result.content)
