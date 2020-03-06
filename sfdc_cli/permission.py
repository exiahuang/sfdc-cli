import os
from . import logging
from . import baseutil
from .setting import SfBasicConfig
from .permission_util import FiledPermissionUtil


class Permission():

    def __init__(self, project_dir=None):
        self.sf_basic_config = SfBasicConfig(project_dir)
        self.settings = self.sf_basic_config.get_setting()

    def list_fields(self, sobject_meta_dir):
        print("\n".join([
            str(data["key"])
            for data in FiledPermissionUtil(sobject_meta_dir).get_all_fields()
        ]))

    def list_sobjects(self, sobject_meta_dir):
        print("\n".join(
            FiledPermissionUtil(sobject_meta_dir).get_all_sobjects()))

    def build(self,
              sobject_meta_dir,
              permission_save_path,
              include_all_sobject_permission=True,
              field_list=None):
        if not os.path.isdir(sobject_meta_dir):
            print("please check sobjects metadata dir!")
            return
        permissionUtil = FiledPermissionUtil(sobject_meta_dir)
        file_path, file_name = os.path.split(permission_save_path)
        name, file_extension = os.path.splitext(file_name)
        if not field_list:
            field_list = [
                str(data["key"]) for data in permissionUtil.get_all_fields()
            ]
        permission_xml = permissionUtil.get_fieldPermission(
            permission_name=name,
            is_all_sobject_permission=include_all_sobject_permission,
            sel_field_list=field_list)
        baseutil.save_file(permission_save_path, permission_xml)
        print(permission_save_path)
