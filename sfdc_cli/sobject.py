import sys, os, shutil, json
from .setting import SfBasicConfig
from . import util, baseutil
from .salesforce import Soap
from . import logging
import xlsxwriter


class SobjectApi():

    def __init__(self, project_dir=None):
        self.sf_basic_config = SfBasicConfig(project_dir)
        self.settings = self.sf_basic_config.get_setting()

    def desc(self, name):
        try:
            sf = util.sf_login(self.sf_basic_config)
            sftype = sf.get_sobject(name)
            messages = []
            tplt = "|{0:<50}|{1:<50}|{2:<5}|{3:<5}|{4:<5}|"
            messages.append(
                tplt.format('name', 'label', 'type', 'length', 'scale'))
            messages.append(
                tplt.format(':---:', ':---:', ':---:', ':---:', ':---:'))
            sftypedesc = sftype.describe()
            for field in sftypedesc["fields"]:
                messages.append(
                    tplt.format(baseutil.xstr(field["name"]),
                                baseutil.xstr(field["label"]),
                                baseutil.xstr(field["type"]),
                                baseutil.xstr(field["length"]),
                                baseutil.xstr(field["scale"])))
            print("\n".join(messages))
        except Exception as e:
            logging.error(e)
            return

    def list(self):
        try:
            sf = util.sf_login(self.sf_basic_config)
            messages = []
            tplt = "|{0:<50}|{1:<50}|{2:<5}|"
            messages.append(tplt.format('label', 'name', 'keyPrefix'))
            messages.append(tplt.format(':---:', ':---:', ':---:'))
            for obj_meta in sf.describe()["sobjects"]:
                messages.append(
                    tplt.format(baseutil.xstr(obj_meta["label"]),
                                baseutil.xstr(obj_meta["name"]),
                                baseutil.xstr(obj_meta["keyPrefix"])))
            print("\n".join(messages))
        except Exception as e:
            logging.error(e)
            return

    def export_xlsx(self,
                    savePath,
                    include_custom_sobject=True,
                    include_standard_sobject=True):
        try:
            dirPath = os.path.dirname(savePath)
            baseutil.makedir(dirPath)
            sf = util.sf_login(self.sf_basic_config)

            sfdesc = sf.describe()
            book = xlsxwriter.Workbook(savePath)
            newSheet_1Name = 'sobject_list'
            newSheet_1 = book.add_worksheet(newSheet_1Name)
            newSheet_1.write(0, 0, 'label')
            newSheet_1.write(0, 1, 'name')
            newSheet_1.write(0, 2, 'keyPrefix')
            index = 1
            sheetIndexMap = {}
            sheetIndex = 0
            sheetIndexMap[0] = newSheet_1Name
            sheetNameList = []
            headers = [
                'name', 'label', 'type', 'length', 'scale', 'updateable',
                'unique', 'custom', 'picklistValues', 'aggregatable',
                'autoNumber', 'byteLength', 'calculated', 'calculatedFormula',
                'cascadeDelete', 'caseSensitive', 'controllerName',
                'createable', 'defaultValue', 'defaultValueFormula',
                'defaultedOnCreate', 'dependentPicklist', 'deprecatedAndHidden',
                'digits', 'displayLocationInDecimal', 'encrypted', 'externalId',
                'extraTypeInfo', 'filterable', 'filteredLookupInfo',
                'groupable', 'highScaleNumber', 'htmlFormatted', 'idLookup',
                'inlineHelpText', 'mask', 'maskType', 'nameField',
                'namePointing', 'nillable', 'permissionable', 'precision',
                'queryByDistance', 'referenceTargetField', 'referenceTo',
                'relationshipName', 'relationshipOrder', 'restrictedDelete',
                'restrictedPicklist', 'soapType', 'sortable',
                'writeRequiresMasterRead'
            ]

            for obj_meta in sf.describe()["sobjects"]:
                #write to xls
                # book.get_sheet(0)
                newSheet_1.write(index, 0, baseutil.xstr(obj_meta["label"]))
                newSheet_1.write(index, 1, baseutil.xstr(obj_meta["name"]))
                newSheet_1.write(index, 2, baseutil.xstr(obj_meta["keyPrefix"]))
                index = index + 1
                if (obj_meta["custom"] and
                        include_custom_sobject) or (not obj_meta["custom"] and
                                                    include_standard_sobject):
                    sheetIndex += 1

                    # sftype = SFType(baseutil.xstr(obj_meta["name"]), sf.session_id, sf.sf_instance, sf_version=sf.sf_version,
                    #               proxies=sf.proxies, session=sf.session)
                    sftype = sf.get_sobject(baseutil.xstr(obj_meta["name"]))

                    #print(obj_meta["name"])
                    #write to xls
                    worksheet_name = baseutil.get_excel_sheet_name(
                        obj_meta["label"])
                    if worksheet_name in sheetNameList:
                        worksheet_name = (obj_meta["label"]
                                         )[0:25] + "_" + baseutil.random_str(4)

                    sheetNameList.append(worksheet_name)

                    fieldSheet_1 = book.add_worksheet(worksheet_name)

                    fieldSheet_1.write(0, 0, 'sobject')
                    fieldSheet_1.write(0, 1, obj_meta["name"])
                    fieldSheet_1.write(1, 0, 'label')
                    fieldSheet_1.write(1, 1, obj_meta["label"])
                    fieldSheet_1.write(2, 0, 'keyPrefix')
                    fieldSheet_1.write(2, 1, obj_meta["keyPrefix"])

                    # book.get_sheet(sheetIndex)
                    rowIndex = 4
                    headerIndex = 0
                    for header in headers:
                        fieldSheet_1.write(rowIndex, headerIndex, header)
                        headerIndex = headerIndex + 1

                    sftypedesc = sftype.describe()
                    for field in sftypedesc["fields"]:
                        rowIndex += 1
                        headerIndex = 0
                        for header in headers:
                            if header == "picklistValues":
                                picklistValuesStr = ''
                                for pv in field[header]:
                                    if 'label' in pv and 'value' in pv:
                                        picklistValuesStr += str(
                                            pv['label']) + ':' + str(
                                                pv['value']) + '\n'
                                fieldSheet_1.write(rowIndex, headerIndex,
                                                   picklistValuesStr)
                            else:
                                fieldSheet_1.write(rowIndex, headerIndex,
                                                   baseutil.xstr(field[header]))
                            headerIndex = headerIndex + 1
            book.close()
            print("export done: %s" % savePath)
        except Exception as e:
            logging.error(e)
            return

    def _print_result(self, data):
        print(json.dumps(data, indent=4, ensure_ascii=False))

    def create(self, sobject, data):
        try:
            sf = util.sf_login(self.sf_basic_config)
            self._print_result(sf.get_sobject(sobject).create(data))
        except Exception as e:
            logging.error(e)
            return

    def update(self, sobject, sid, data):
        try:
            sf = util.sf_login(self.sf_basic_config)
            self._print_result(sf.get_sobject(sobject).update(sid, data))
        except Exception as e:
            logging.error(e)
            return

    def delete(self, sobject, sid):
        try:
            sf = util.sf_login(self.sf_basic_config)
            self._print_result(sf.get_sobject(sobject).delete(sid))
        except Exception as e:
            logging.error(e)
            return

    def get(self, sobject, sid):
        try:
            sf = util.sf_login(self.sf_basic_config)
            self._print_result(sf.get_sobject(sobject).get(sid))
        except Exception as e:
            logging.error(e)
            return
