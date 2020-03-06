import os
from .setting import SfBasicConfig
from . import util, baseutil
from . import logging
from . import codecreator


class Coder():

    def __init__(self, project_dir=None):
        self.sf_basic_config = SfBasicConfig(project_dir)
        self.settings = self.sf_basic_config.get_setting()

    def soql_creater(self,
                     objectApiName,
                     is_custom_only=True,
                     is_updateable=True,
                     include_relationship=True,
                     include_comment=True):
        try:
            sf = util.sf_login(self.sf_basic_config)
            sftype = sf.get_sobject(objectApiName)
            sftypedesc = sftype.describe()
            soql = codecreator.get_soql_src(
                objectApiName,
                sftypedesc["fields"],
                sf,
                condition='',
                has_comment=include_comment,
                is_custom_only=is_custom_only,
                updateable_only=is_updateable,
                include_relationship=include_relationship)
            print(soql)
        except Exception as e:
            logging.error(e)
            return

    def _createTestDataStr(self, objectApiName, sftype, isAllField):
        obj_name = baseutil.get_obj_name(objectApiName)
        message = ("List<{T}> {objName}List = new List<{T}>();\n".format(
            T=objectApiName, objName=obj_name))
        message += "for(Integer i=0; i<5; i++){\n"
        message += ("\t{T} {objName} = new {T}();\n".format(T=objectApiName,
                                                            objName=obj_name))

        sftypedesc = sftype.describe()
        for field in sftypedesc["fields"]:
            ## https://developer.salesforce.com/docs/atlas.en-us.api.meta/api/sforce_api_calls_describesobjects_describesobjectresult.htm#topic-title
            ## obj type
            if isAllField:
                check = field["updateable"] and field["name"] != 'OwnerId'
            else:
                check = field["updateable"] \
                        and not field["nillable"] \
                        and field["name"] != 'OwnerId'\
                        and ( field["defaultValue"] is None ) \
                        and ( field["type"] != 'boolean' )

            if check:
                # if field["updateable"]:
                ## do with picklist
                picklistValues = []
                if field["type"] == 'picklist' or field[
                        "type"] == 'multipicklist':
                    for pv in field['picklistValues']:
                        picklistValues.append(pv['value'])
                if field["type"] == 'int' or field["type"] == 'double' or field[
                        "type"] == 'currency':
                    length = field["length"] if field["length"] < 3 else 3
                else:
                    length = field["length"] if field["length"] < 8 else 8
                val = baseutil.random_data(data_type=field["type"],
                                           length=length,
                                           scale=field["scale"],
                                           filed_name=field["name"],
                                           picklistValues=picklistValues)
                message += (
                    "\t{objName}.{field} = {value};    //{label}\n".format(
                        objName=obj_name,
                        field=baseutil.xstr(field["name"]),
                        value=val,
                        label=field["label"],
                    ))
        message += ("\t{objName}List.add({objName});\n".format(
            T=objectApiName, objName=obj_name))
        message += "}\n"
        message += ("insert {objName}List;\n\n".format(objName=obj_name))
        return message

    def insert_data_snippet(self, objectApiName, is_all_field=False):
        try:
            sf = util.sf_login(self.sf_basic_config)
            sample_data = self._createTestDataStr(
                objectApiName=objectApiName,
                sftype=sf.get_sobject(objectApiName),
                isAllField=is_all_field)
            print(sample_data)
        except Exception as e:
            logging.error(e)
            return

    def insert_data_snippet_from_soql(self, soql):
        try:
            sf = util.sf_login(self.sf_basic_config)
            soql_result = sf.query(soql)
            object_name = baseutil.get_query_object_name(soql_result)
            if object_name:
                sftype = sf.get_sobject(object_name)
                sftypedesc = sftype.describe()
                fields = {}
                for field in sftypedesc["fields"]:
                    name = field['name'].lower()
                    fields[name] = field
                message = baseutil.get_soql_to_apex(fields, soql, soql_result)
            else:
                message = 'Query Error!\n'
            print(message)
        except Exception as e:
            logging.error(e)
            return

    def create_testclass(self, apexfile):
        try:
            sf = util.sf_login(self.sf_basic_config)
            if not os.path.isfile(apexfile) and (apexfile.find(".cls") > -1):
                print('Error file type! Please select a cls file.')
                return
            test_code, sfdc_name_map = codecreator.get_testclass(
                baseutil.read_file(apexfile))
            save_file_path = os.path.join(os.path.dirname(apexfile),
                                          sfdc_name_map['test_class_file'])
            baseutil.save_file(save_file_path, test_code)
            baseutil.save_file(
                os.path.join(save_file_path + '-meta.xml'),
                codecreator.get_meta_xml("ApexClass",
                                         sfdc_name_map['test_class_file'],
                                         self.settings["api_version"]))
            print(save_file_path)
        except Exception as e:
            logging.error(e)
            return

    #Create VisualForce/Controller/DTO/DAO Code
    def create_sfdc_code(self,
                         objectApiName,
                         save_dir,
                         is_custom_only=True,
                         include_validate=True):
        try:
            sf = util.sf_login(self.sf_basic_config)
            sftype = sf.get_sobject(objectApiName)
            sftypedesc = sftype.describe()

            classes_dir = os.path.join(save_dir, "classes")
            pages_dir = os.path.join(save_dir, "pages")
            sfdc_name_map = codecreator.get_sfdc_namespace(objectApiName)

            is_open = False
            save_path_list = []

            api_version = self.settings["api_version"]

            # dto Code
            logging.info('start to build dto')
            dto_code, class_name = codecreator.get_dto_class(
                objectApiName, sftypedesc["fields"], is_custom_only,
                include_validate)
            file_name = sfdc_name_map['dto_file']
            baseutil.save_file(os.path.join(classes_dir, file_name), dto_code)
            baseutil.save_file(
                os.path.join(classes_dir, file_name + '-meta.xml'),
                codecreator.get_meta_xml("ApexClass", class_name, api_version))
            save_path_list.append(os.path.join(classes_dir, file_name))

            # dao Code
            logging.info('start to build dao')
            dao_code = codecreator.get_dao_class(objectApiName,
                                                 sftypedesc["fields"], sf,
                                                 is_custom_only)
            file_name = sfdc_name_map['dao_file']
            baseutil.save_file(os.path.join(classes_dir, file_name), dao_code)
            baseutil.save_file(
                os.path.join(classes_dir, file_name + '-meta.xml'),
                codecreator.get_meta_xml("ApexClass", class_name, api_version))
            save_path_list.append(os.path.join(classes_dir, file_name))

            # controller code
            logging.info('start to build controller')
            controller_code, class_name = codecreator.get_controller_class(
                objectApiName)
            file_name = sfdc_name_map['controller_file']
            baseutil.save_file(os.path.join(classes_dir, file_name),
                               controller_code)
            baseutil.save_file(
                os.path.join(classes_dir, file_name + '-meta.xml'),
                codecreator.get_meta_xml("ApexClass", class_name, api_version))
            save_path_list.append(os.path.join(classes_dir, file_name))

            # visualforce code
            logging.info('start to build visualforce')
            vf_code, class_name = codecreator.get_vf_class(
                objectApiName, sftypedesc["fields"], is_custom_only,
                include_validate)
            file_name = sfdc_name_map['vf_file']
            baseutil.save_file(os.path.join(pages_dir, file_name), vf_code)
            baseutil.save_file(
                os.path.join(pages_dir, file_name + '-meta.xml'),
                codecreator.get_meta_xml("ApexPage", class_name, api_version))
            save_path_list.append(os.path.join(pages_dir, file_name))

            # list controller code
            logging.info('start to build list controller')
            list_controller_code, class_name = codecreator.get_list_controller_class(
                objectApiName)
            file_name = sfdc_name_map['list_controller_file']
            baseutil.save_file(os.path.join(classes_dir, file_name),
                               list_controller_code)
            baseutil.save_file(
                os.path.join(classes_dir, file_name + '-meta.xml'),
                codecreator.get_meta_xml("ApexClass", class_name, api_version))
            save_path_list.append(os.path.join(classes_dir, file_name))

            # visualforce code
            logging.info('start to build list visualforce')
            list_vf_code, class_name = codecreator.get_list_vf_class(
                objectApiName, sftypedesc["fields"], is_custom_only,
                include_validate)
            file_name = sfdc_name_map['list_vf_file']
            baseutil.save_file(os.path.join(pages_dir, file_name), list_vf_code)
            baseutil.save_file(
                os.path.join(pages_dir, file_name + '-meta.xml'),
                codecreator.get_meta_xml("ApexPage", class_name, api_version))
            save_path_list.append(os.path.join(pages_dir, file_name))

            # SfdcXyController
            logging.info('start to build SfdcXyController')
            src_code = codecreator.get_sfdcxycontroller()
            file_name = 'SfdcXyController.cls'
            baseutil.save_file(os.path.join(classes_dir, file_name),
                               list_controller_code)
            baseutil.save_file(
                os.path.join(classes_dir, file_name + '-meta.xml'),
                codecreator.get_meta_xml("ApexClass", class_name, api_version))
            save_path_list.append(os.path.join(classes_dir, file_name))

            print("create code done!")
            print("\n".join(save_path_list))

        except Exception as e:
            logging.error(e)
            return
