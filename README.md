# sfdc-cli

[exiahuang/sfdc-cli](https://github.com/exiahuang/sfdc-cli) is a sfdc development kit.
It is licensed under the `Apache License 2.0`

## preface

I build a sublime plugin [exiahuang/SalesforceXyTools](https://github.com/exiahuang/SalesforceXyTools) for sfdc 3 year ago.
I use this code, and turn it to command line.

## feature

-   TODO: integrate with [exiahuang/xysfdx](https://github.com/exiahuang/xysfdx), and run in vscode.
-   use python3

# install

## install from pip

TODO: not work now.

```sh
pip3 install sfdc-cli
```

## install from git

```sh
git clone https://github.com/exiahuang/sfdc-cli
python3 setup.py install
```

# Usage

## print help

```sh
sfdc -h
```

```
usage: sfdc [-h]

sfdc development kit v0.1.0

positional arguments:

    apex:test:coverage  see `apex:test:coverage -h`
    data:soql:query     see `data:soql:query -h`
    meta:new            see `meta:new -h`
    folder:list         see `folder:list -h`
    ant:migration:tool  see `ant:migration:tool -h`
    meta:update         see `meta:update -h`
    meta:template:component
                        see `meta:template:component -h`
    sobject:data:delete
                        see `sobject:data:delete -h`
    meta:template:apex  see `meta:template:apex -h`
    coder:apex:testclass:generator
                        see `coder:apex:testclass:generator -h`
    packagexml:local    see `packagexml:local -h`
    apex:execute        see `apex:execute -h`
    coder:apex:snippet:insert:ramdam:data
                        see `coder:apex:snippet:insert:ramdam:data -h`
    sobject:export:xlsx
                        see `sobject:export:xlsx -h`
    meta:attr           see `meta:attr -h`
    sobject:data:create
                        see `sobject:data:create -h`
    download:attachment
                        see `download:attachment -h`
    coder:apex:page:generator
                        see `coder:apex:page:generator -h`
    meta:refresh:dir    see `meta:refresh:dir -h`
    sobject:fields:desc
                        see `sobject:fields:desc -h`
    tools:json:format   json format
    meta:retrieve       see `meta:retrieve -h`
    coder:permission:build
                        see `coder:permission:build -h`
    sobject:data:get    see `sobject:data:get -h`
    data:tooling:query  see `data:tooling:query -h`
    meta:cache          see `meta:cache -h`
    coder:apex:snippet:insert:data:from:soql
                        see `coder:apex:snippet:insert:data:from:soql -h`
    coder:copy:aura     see `coder:copy:aura -h`
    apex:test:run       see `apex:test:run -h`
    coder:permission:list
                        see `coder:permission:list -h`
    meta:refresh        see `meta:refresh -h`
    project:init        see `project:init -h`
    meta:refresh:aura   see `meta:refresh:aura -h`
    call:rest:api       see `call:rest:api -h`
    meta:template:page  see `meta:template:page -h`
    meta:delete         see `meta:delete -h`
    sobject:data:update
                        see `sobject:data:update -h`
    packagexml:server   see `packagexml:server -h`
    sobject:list        see `sobject:list -h`
    meta:template:trigger
                        see `meta:template:trigger -h`
    coder:snippet:soql  see `coder:snippet:soql -h`
    help                see `help -h`

optional arguments:
  -h, --help            show this help message and exit
```

## new project

```sh
# for product
sfdc project:init -d project/sfdc-project1 -u username -p password -t security_token -s src -v api_version
# for sandbox/stgfull
sfdc project:init -d project/sfdc-project1 -u username -p password -t security_token -s src -v api_version --sandbox

cd project/sfdc-project1
```

## metadata retrieve

```sh
# retrieve zip file of all metadata
sfdc meta:retrieve -p . -d package_dir -n package.zip

# retrieve zip file of choice metadata : ApexClass ApexTrigger ApexPage
sfdc meta:retrieve -p . -d package_dir -n package1.zip -m ApexClass ApexTrigger ApexPage ApexComponent CustomObject

# retrieve metadata and unzip, source path: src
sfdc meta:retrieve -p . -d package_dir -n package2.zip -m ApexClass ApexTrigger ApexPage AuraDefinitionBundle LightningComponentBundle --unzip --delete_after_unzip


sfdc meta:retrieve -p . -d package_dir -n package2.zip -m CustomObject --unzip --delete_after_unzip

sfdc meta:retrieve -p . -d package_dir -n package2.zip -m PermissionSet --unzip --delete_after_unzip
```

## metadata template

### init apex class from template

```sh
sfdc meta:template:apex -n HelloApex --template ApexClass.cls
sfdc meta:template:apex -n HelloApexBatch --template BatchApexClass.cls
sfdc meta:template:apex -n HelloApexTest --template UnitTestApexClass.cls
sfdc meta:template:apex -n HelloApexBatchTest --template BDDUnitTestApexClass.cls
```

### init trigger from template

```sh
sfdc meta:template:trigger -n HelloApexTrigger --sobject Opportunity --template ApexTrigger.trigger
sfdc meta:template:trigger -n HelloApexTriggerAllEvents --sobject Opportunity --template ApexTriggerAllEvents.trigger
sfdc meta:template:trigger -n HelloApexTriggerBulk --sobject Opportunity --template ApexTriggerBulk.trigger
```

### init visualforce from template

```sh
sfdc meta:template:page -n HelloApexPage --template ApexPage.page
sfdc meta:template:page -n HelloHeaderPageBlock --template HeaderPageBlock.page
```

### init visualforce component

```sh
sfdc meta:template:component -n HelloCmp
```

## metadata new/update/refresh/delete

### new metadata

```sh
sfdc meta:new -p . -s ./src/classes/HelloApex.cls
sfdc meta:new -p . -s ./src/classes/HelloApexBatch.cls
sfdc meta:new -p . -s ./src/classes/HelloApexTest.cls
sfdc meta:new -p . -s ./src/classes/HelloApexBatchTest.cls
sfdc meta:new -p . -s ./src/pages/HelloApexPage.page
sfdc meta:new -p . -s ./src/components/HelloCmp.component
sfdc meta:new -p . -s ./src/triggers/HelloApexTrigger.trigger --sobject Opportunity
sfdc meta:new -p . -s ./src/triggers/HelloApexTriggerAllEvents.trigger --sobject Opportunity
sfdc meta:new -p . -s ./src/triggers/HelloApexTriggerBulk.trigger --sobject Opportunity
```

### update metadata

```sh
sfdc meta:update -p . -s ./src/classes/HelloApex.cls
sfdc meta:update -p . -s ./src/classes/HelloApexBatch.cls
sfdc meta:update -p . -s ./src/classes/HelloApexTest.cls
sfdc meta:update -p . -s ./src/classes/HelloApexBatchTest.cls
sfdc meta:update -p . -s ./src/pages/HelloApexPage.page
sfdc meta:update -p . -s ./src/components/HelloCmp.component
sfdc meta:update -p . -s ./src/triggers/HelloApexTrigger.trigger
sfdc meta:update -p . -s ./src/triggers/HelloApexTriggerAllEvents.trigger
sfdc meta:update -p . -s ./src/triggers/HelloApexTriggerBulk.trigger
```

### metadata refresh

#### metadata refresh by filepath

```sh
# refresh apex/trigger/page/copmonent/ aura file
sfdc meta:refresh -p . -s src/classes/HelloApex.cls
sfdc meta:refresh -p . -s ./src/classes/HelloApex.cls
sfdc meta:refresh -p . -s ./src/classes/HelloApexBatch.cls
sfdc meta:refresh -p . -s ./src/aura/HelloWorld/HelloWorld.cmp
sfdc meta:refresh -p . -s ./src/aura/HelloWorld/HelloWorld.css
sfdc meta:refresh -p . -s ./src/aura/HelloWorld
```

#### metadata refresh by directory

support directorys, [read more](README.meta-refresh.md)

```sh

# refresh directory, examples
sfdc meta:refresh:dir -p . -d ./src/classes
sfdc meta:refresh:dir -p . -d ./src/triggers
sfdc meta:refresh:dir -p . -d ./src/components
sfdc meta:refresh:dir -p . -d ./src/pages
sfdc meta:refresh:dir -p . -d ./src/layouts
sfdc meta:refresh:dir -p . -d ./src/lwc
sfdc meta:refresh:dir -p . -d ./src/aura

# refresh one aura componet
sfdc meta:refresh:aura -p . -s ./src/aura/HelloWorld

```

### delete metadata

```sh
sfdc meta:delete -p . -s ./src/classes/HelloApex.cls
sfdc meta:delete -p . -s ./src/classes/HelloApexBatch.cls
sfdc meta:delete -p . -s ./src/classes/HelloApexTest.cls
sfdc meta:delete -p . -s ./src/classes/HelloApexBatchTest.cls
sfdc meta:delete -p . -s ./src/pages/HelloApexPage.page
sfdc meta:delete -p . -s ./src/components/HelloCmp.component
sfdc meta:delete -p . -s ./src/triggers/HelloApexTrigger.trigger
```

## metadata attribute

```sh
sfdc meta:attr -p . -s ./src/classes/HelloApex.cls
```

## package.xml

### build from server

```sh
# build package in current directory, filename package.xml
sfdc packagexml:server

sfdc packagexml:server -p . -d . -n package.xml
```

### build from local

scan directory and build package.xml

```sh
sfdc packagexml:local --scandir ./src --savedir . -n package.xml
```

## sfdc apex

### Executes anonymous Apex code

```sh
# create a apex code
mkdir ./tmp/
echo "System.debug('hello world');" > ./tmp/HelloApex.apex

# run the apex code
sfdc apex:execute -p . -s ./tmp/HelloApex.apex

# use pipe
cat ./tmp/HelloApex.apex | sfdc apex:execute -p .
```

### run apex testclass

```sh
sfdc apex:test:run -p . -s ./src/classes/HelloApexTest.cls
sfdc apex:test:run -p . -s ./src/classes/HelloApexBatchTest.cls
```

### get coverage

```sh
sfdc apex:test:coverage -p . -f ./log/apex_coverage.log
```

## sobject

### create sobject data

```sh
# insert a account
echo "{\"Name\":\"exiahuang\"}" | sfdc sobject:data:create -s Account

# use json_data_file to create sobject data
sfdc sobject:data:create -s Account --data $json_data_file_path

```

### get sobject data

```sh
sfdc sobject:data:get -s Account --id $account_id
```

### delete sobject data

```sh
sfdc sobject:data:delete -s Account --id $account_id
```

### update sobject data

```sh
# update sobject data from pipe
echo "{\"Phone\":\"080-0000-0000\"}" | sfdc sobject:data:update -s Account --id $account_id

# update sobject data from json file
sfdc sobject:data:update -s Account --id $account_id --data $json_data_file_path
```

### list sobject

```sh
cd $project_dir
# print in console
sfdc sobject:list

# save as markdown file
sfdc sobject:list > log/sobject.md
```

### export sobject as xlsx file

```sh
cd $project_dir
sfdc sobject:export:xlsx -s log/sobject.xlsx
```

### describe fields

```sh
sfdc sobject:fields:desc -s $sobject_name
```

## data query

### soql query

```sh
sfdc data:soql:query -s "SELECT id,name from USER limit 10"
```

### tooling query

```sh
sfdc data:tooling:query -s "SELECT Id,Name FROM ApexClass limit 100"
```

## call salesforce rest api

### Get method

```sh
# call /services/data/v45.0/sobjects
sfdc call:rest:api -e /services/data/v45.0/sobjects

# call /services/data/v45.0/sobjects/Account
sfdc call:rest:api -e /services/data/v45.0/sobjects/Account
sfdc call:rest:api -e /services/data/v45.0/sobjects/Opportunity

```

### use file as params

```sh
echo '{"q": "Select Id, Name From ApexClass Limit 3"}' > tmp/sf_rest_test.json
sfdc call:rest:api -m GET -e /services/data/v45.0/tooling/query --use_params --params tmp/sf_rest_test.json
```

### use pipe to call rest api

example : query ApexCodeCoverage

```sh
# example1 : query ApexCodeCoverage
echo '{"q": "SELECT Id, ApexTestClassId, TestMethodName, ApexClassorTriggerId, NumLinesCovered, NumLinesUncovered, Coverage FROM ApexCodeCoverage"}' | sfdc call:rest:api -m GET -e /services/data/v45.0/tooling/query --use_params


# example1 : query ApexClass
echo '{"q": "Select Id, Name From ApexClass Limit 3"}' | sfdc call:rest:api -m GET -e /services/data/v45.0/tooling/query --use_params
```

## code creator

### create soql

```sh
#
sfdc coder:snippet:soql -s $sobject_name --custom_field_only --updateable_field_only --include_comment --include_relationship

#
sfdc coder:snippet:soql -s Account  --custom_field_only --updateable_field_only --include_comment --include_relationship
```

### insert sobject data code snippet from soql

```sh
sfdc coder:apex:snippet:insert:data:from:soql -s $soql
sfdc coder:apex:snippet:insert:data:from:soql -s "SELECT name, firstname, lastname FROM Account LIMIT 2"
```

### insert sobject data code snippet

```sh
sfdc coder:apex:snippet:insert:ramdam:data -s $sobject_name --all_fields
sfdc coder:apex:snippet:insert:ramdam:data -s Account --all_fields

```

### generator testclass from apex

```sh
sfdc coder:apex:testclass:generator -f $apex_code_file_path
```

### generator VisualForce/Controller/DTO/DAO Code from sobject

```sh
sfdc coder:apex:page:generator --sobject $sobject_name --savedir tmp/mycode/src --custom_field_only --include_validate
```

### copy lightning

```sh
sfdc coder:copy:aura -f $from_lightning_path -t $to_lightning_path
sfdc coder:copy:aura -f /app/project/sfdc-project1/src/aura/HelloWorld -t /app/project/sfdc-project1/src/aura/HelloWorld1
```

### create permission metadata

retrieve sobject metadata first

```sh
# retrieve sobject metadata
sfdc meta:retrieve -p . -d package_dir -n package2.zip -m CustomObject --unzip --delete_after_unzip
# or use meta:refresh:dir
sfdc meta:refresh:dir -p . -d ./src/objects
```

create permission from sobject metadata

```sh
# include sobject permission and all fields permission
sfdc coder:permission:build --sobject_dir ./src/objects --savefile ./src/permissionsets/dev_permission.permissionset --include_all_sobject_permission

# fieldPermissions
sfdc coder:permission:build --sobject_dir ./src/objects --savefile ./src/permissionsets/dev_permission.permissionset --fields Account.custom_field1 Account.custom_field2 Opportunity.custom_field1
```

list fields from sobject metadata directory

```sh
# list fields
sfdc coder:permission:list -t fields --sobject_dir ./src/objects

sfdc coder:permission:list -t fields --sobject_dir ./src/objects | grep Account

```

list sobject from sobject metadata directory

```
# list sobject
sfdc coder:permission:list -t sobject --sobject_dir ./src/objects

```

## salesforce folder

```sh
# report folder
sfdc folder:list -n ReportFolder

# email folder
sfdc folder:list -n EmailTemplate
```

## download salesforce attachment

download salesforce attachment(ContentVersion):

-   max limit size: 2000
-   default filename template: `{Id}_{Title}_v{VersionNumber}.{FileExtension}`

```sh
sfdc download:attachment --savedir tmp/download --filename "{Title}_v{VersionNumber}.{FileExtension}" --limit 2000
```

## Ant Migration Tool

### init Ant Migration Tool

```sh
sfdc ant:migration:tool
# or
sfdc ant:migration:tool -p .
```

## tools

### json format

```sh
cat $json_file_path | sfdc tools:json:format

sfdc tools:json:format -i $json_file_path
```

# For developer

## Set up docker

```sh
# for windows user
docker run --rm -it -v %cd%:/app -w=/app -e TZ=Asia/Tokyo --name sfdc-cli_developer_1 python:3.8 bash
# for linux/mac
docker run --rm -it -v `pwd`:/app -w=/app -e TZ=Asia/Tokyo --name sfdc-cli_developer_1 python:3.8 bash

# git clone
git clone https://github.com/exiahuang/sfdc-cli

# setup
cd sfdc-cli
pip3 install -r requirement.dev.txt
python3 -m sfdc_cli.cli
alias sfdc="python3 -m sfdc_cli.cli"
export PYTHONPATH="/app/sfdc-cli:$PYTHONPATH"
sfdc -h

# remove commmand
unalias sfdc

```

## remove pycache

```sh
### use find
find . | grep -E "(__pycache__|\.pyc|\.pyo$)" | xargs rm -rf
### use py3clean
py3clean .
```

## Run test case.

### new project

```sh
python3 -m unittest tests.test_project
```

### init from template

```sh
python3 -m unittest tests.test_metadata_template
```

### sfdc metadata api

```sh
# new apex/trigger/page/component template
python3 -m unittest tests.test_metadata_template

# metadata api: new metadata
python3 -m unittest tests.test_metadata_api.MetadataApiNewMetaTestCase.test_metadata_new

# metadata api: reload cache
python3 -m unittest tests.test_metadata_api.MetadataApiNewMetaTestCase.test_metadata_cache

# metadata api: update metadata
python3 -m unittest tests.test_metadata_api.MetadataApiUpdateTestCase.test_metadata_update

# metadata api: update aura metadata
python3 -m unittest tests.test_metadata_api.MetadataApiUpdateTestCase.test_metadata_update_arua

# metadata api: refresh metadata
python3 -m unittest tests.test_metadata_api.MetadataApiRefreshTestCase

# metadata api: refresh aura metadata
python3 -m unittest tests.test_metadata_api.MetadataApiRefreshAuraTestCase

# metadata api: print attr
python3 -m unittest tests.test_metadata_api.MetadataApiAttrTestCase

# delete metadata
python3 -m unittest tests.test_metadata_api.MetadataApiDeleteTestCase

# test delete aura
python3 -m unittest tests.test_metadata_api.MetadataApiDeleteTestCase.test_metadata_delete_arua

# run testclass
python3 -m unittest tests.test_testclass.TestclassTestCase.test_run_test

# run retrieve apex coverage
python3 -m unittest tests.test_testclass.TestclassTestCase.test_retrieve_apex_coverage

# retrieve zip
python3 -m unittest tests.test_metadata_api.RetrieveApiTestCase

# package xml : retrieve from server
python3 -m unittest tests.test_package_xml.PackageXmlTestCase.test_package_xml_from_server

# package xml : build from local
python3 -m unittest tests.test_package_xml.PackageXmlTestCase.test_package_xml_from_dir

# open in browser
python3 -m unittest tests.test_browser.BrowserTestCase.test_open_src
python3 -m unittest tests.test_browser.BrowserTestCase.test_open_aura

# open in browser : open sobject
python3 -m unittest tests.test_browser.BrowserTestCase.test_open_account_sobject
python3 -m unittest tests.test_browser.BrowserTestCase.test_open_opp_sobject


```

### sfdc file attribute

```sh
# file attr
# file attr
python3 -m unittest tests.test_metadata_api.FileAttrTestCase
```

result:

```json
{
  "name": "MyApexController",
  "file_path": "project/sfdc-projcet1/src/classes",
  "file_name": "MyApexController.cls",
  "dir": "classes",
  "p_dir": "src",
  "extension": "cls",
  "metadata_type": "ApexClass",
  "metadata_folder": "classes",
  "metadata_sub_folder": "",
  "is_sfdc_file": true,
  "is_src": true,
  "is_lux": false,
  "is_lux_root": false,
  "is_lwc": false,
  "is_lwc_root": false,
  "lux_type": "",
  "lux_name": "",
  "file_key": "classes/MyApexController.cls"
}


{
  "name": "HelloWorld",
  "file_path": "project/sfdc-projcet1/src/aura/HelloWorld",
  "file_name": "HelloWorld.cmp",
  "dir": "HelloWorld",
  "p_dir": "aura",
  "extension": "cmp",
  "metadata_type": "AuraDefinition",
  "metadata_folder": "aura",
  "metadata_sub_folder": "HelloWorld",
  "is_sfdc_file": true,
  "is_src": false,
  "is_lux": true,
  "is_lux_root": false,
  "is_lwc": false,
  "is_lwc_root": false,
  "lux_type": "COMPONENT",
  "lux_name": "HelloWorld",
  "file_key": "aura/HelloWorld/HelloWorld.cmp"
}
```

# package

```sh
python3 setup.py sdist
python3 setup.py bdist_wininst
```

# Acknowledgement

## Basic on OpenSource

1. [xlsxwriter (License: BSD)](https://github.com/jmcnamara/XlsxWriter)
2. [Simple-Salesforce (License: Apache 2.0)](https://pypi.python.org/pypi/simple-salesforce/0.72.2)
3. [requests (License: Apache 2.0)](https://pypi.python.org/pypi/requests/2.12.3)
4. [Apex Template From MavensMate](https://github.com/joeferraro/MavensMate/tree/master/app/lib/templates/github)
