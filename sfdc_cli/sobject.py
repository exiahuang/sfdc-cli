import sys, os, shutil
from .setting import SfBasicConfig
from . import util, baseutil
from .salesforce import (ToolingApi,
                         MetadataApi)
from . import logging
import xlsxwriter

class SobjectApi():

    def __init__(self, project_dir=None):
        self.sf_basic_config = SfBasicConfig(project_dir)
        self.settings = self.sf_basic_config.get_setting()

    def list(self):
        try:
            sf = util.sf_login(self.sf_basic_config)
            messages = []
            tplt = "|{0:<50}|{1:<50}|{2:<5}|"
            messages.append(tplt.format('label', 'name', 'keyPrefix'))
            messages.append(tplt.format(':---:', ':---:', ':---:'))
            for x in sf.describe()["sobjects"]:
                messages.append(tplt.format(baseutil.xstr(x["label"]), baseutil.xstr(x["name"]), baseutil.xstr(x["keyPrefix"])))
            print("\n".join(messages))
        except Exception as e:
            logging.error(e)
            return

    def export_xlsx(self, savePath, is_all_sobject=True, is_custom_sobject=True, is_standard_sobject=True):
        try:
            dirPath = os.path.dirname(savePath)
            baseutil.makedir(dirPath)
            sf = util.sf_login(self.sf_basic_config)

            sfdesc = sf.describe()
            book = xlsxwriter.Workbook(savePath)
            newSheet_1Name = 'オブジェクトリスト'
            newSheet_1 = book.add_worksheet(newSheet_1Name)
            newSheet_1.write(0, 0, 'label')
            newSheet_1.write(0, 1, 'name')
            newSheet_1.write(0, 2, 'keyPrefix')
            index = 1;

            sheetIndexMap = {}
            sheetIndex = 0;
            sheetIndexMap[0] = newSheet_1Name

            sheetNameList = []

            headers = ['name','label','type','length','scale','updateable','unique','custom','picklistValues','aggregatable','autoNumber','byteLength','calculated','calculatedFormula','cascadeDelete','caseSensitive','controllerName','createable','defaultValue','defaultValueFormula','defaultedOnCreate','dependentPicklist','deprecatedAndHidden','digits','displayLocationInDecimal','encrypted','externalId','extraTypeInfo','filterable','filteredLookupInfo','groupable','highScaleNumber','htmlFormatted','idLookup','inlineHelpText','mask','maskType','nameField','namePointing','nillable','permissionable','precision','queryByDistance','referenceTargetField','referenceTo','relationshipName','relationshipOrder','restrictedDelete','restrictedPicklist','soapType','sortable','writeRequiresMasterRead']

            for x in sf.describe()["sobjects"]:
              #write to xls
              # book.get_sheet(0)
              newSheet_1.write(index, 0, baseutil.xstr(x["label"]))
              newSheet_1.write(index, 1, baseutil.xstr(x["name"]))
              newSheet_1.write(index, 2, baseutil.xstr(x["keyPrefix"]))
              index = index + 1
              #print(sf.Kind__c.describe())
              #print(x["name"])
              #print(x["custom"])
              if is_all_sobject or (x["custom"] and is_custom_sobject) or ( not x["custom"] and is_standard_sobject):
                  sheetIndex += 1
                  
                  # sftype = SFType(baseutil.xstr(x["name"]), sf.session_id, sf.sf_instance, sf_version=sf.sf_version,
                  #               proxies=sf.proxies, session=sf.session)
                  sftype = sf.get_sobject(baseutil.xstr(x["name"]))

                  #print(x["name"])     
                  #write to xls
                  worksheet_name = baseutil.get_excel_sheet_name(x["label"])
                  if worksheet_name in sheetNameList:
                    worksheet_name = (x["label"])[0:25] + "_" + baseutil.random_str(4)
                  
                  sheetNameList.append(worksheet_name)


                  fieldSheet_1 = book.add_worksheet(worksheet_name)

                  fieldSheet_1.write(0, 0, 'sobject')
                  fieldSheet_1.write(0, 1, x["name"])
                  fieldSheet_1.write(1, 0, 'label')
                  fieldSheet_1.write(1, 1, x["label"])
                  fieldSheet_1.write(2, 0, 'keyPrefix')
                  fieldSheet_1.write(2, 1, x["keyPrefix"])

                  # book.get_sheet(sheetIndex)
                  rowIndex = 4;
                  headerIndex = 0
                  for header in headers:
                    fieldSheet_1.write(rowIndex, headerIndex, header)
                    headerIndex = headerIndex + 1

                  sftypedesc = sftype.describe()
                  for field in sftypedesc["fields"]:
                     #print(field)  
                     #print(field["name"])  
                     #print(field["label"])  
                     #print(field["type"])  
                     #print(field["length"])  
                     #print(field["scale"])  
                     rowIndex += 1
                     headerIndex = 0
                     for header in headers:
                        if header == "picklistValues":
                            picklistValuesStr = ''
                            for pv in field[header]:
                                if 'label' in pv and 'value' in pv:
                                    picklistValuesStr += str(pv['label']) + ':' + str(pv['value']) + '\n'
                            fieldSheet_1.write(rowIndex, headerIndex, picklistValuesStr)
                        else:
                            fieldSheet_1.write(rowIndex, headerIndex, baseutil.xstr(field[header]))
                        headerIndex = headerIndex + 1
            print("export done: %s" % dirPath)
        except Exception as e:
            logging.error(e)
            return