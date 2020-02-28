---
categories: sfdc-cli
data: 2020/02/28 20:08:26
tags:
- sfdc
- salesforce
- sfdc-cli
title: Readme
update_date: 2020/02/28 20:16:01

---

# sfdc-cli

[exiahuang/sfdc-cli](https://github.com/exiahuang/sfdc-cli) is a sfdc development kit.
It is licensed under the `Apache License 2.0`

## preface

I build a sublime plugin [exiahuang/SalesforceXyTools](https://github.com/exiahuang/SalesforceXyTools) for sfdc 3 year ago.
I use this code, and turn it to command line.

## feature

-   TODO: integrate with [exiahuang/xysfdx](https://github.com/exiahuang/xysfdx), and run in vscode.
-   use python

# install

## install from pip

TODO: not work now

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

    meta:attr           see `meta:attr -h`
    meta:cache          see `meta:cache -h`
    meta:delete         see `meta:delete -h`
    meta:new            see `meta:new -h`
    meta:refresh        see `meta:refresh -h`
    meta:refresh:aura   see `meta:refresh:aura -h`
    meta:refresh:dir    see `meta:refresh:dir -h`
    meta:retrieve       see `meta:retrieve -h`
    meta:template:apex  see `meta:template:apex -h`
    meta:template:component
                        see `meta:template:component -h`
    meta:template:page  see `meta:template:page -h`
    meta:template:trigger
                        see `meta:template:trigger -h`
    meta:update         see `meta:update -h`
    packagexml:local    see `packagexml:local -h`
    packagexml:server   see `packagexml:server -h`
    project:init        see `project:init -h`
    sobject:list        see `sobject:list -h`
    sobject:xlsx        see `sobject:xlsx -h`
    test:coverage       see `test:coverage -h`
    test:run            see `test:run -h`
    tools:copy:aura     see `tools:copy:aura -h`
    tools:json:format   json format
    help                see `help -h`

optional arguments:
  -h, --help            show this help message and exit
```

## new project

```sh
sfdc project:init -d project/sfdc-project1
cd project/sfdc-project1
```

## metadata retrieve

```sh
# retrieve zip file of all metadata
sfdc meta:retrieve -p . -d package_dir -n package.zip

# retrieve zip file of choice metadata : ApexClass ApexTrigger ApexPage
sfdc meta:retrieve -p . -d package_dir -n package1.zip -m ApexClass ApexTrigger ApexPage ApexComponent CustomObject

# retrieve metadata and unzip, source path: src
sfdc meta:retrieve -p . -d package_dir -n package2.zip -m ApexClass ApexTrigger ApexPage AuraDefinitionBundle LightningComponentBundle --unzip --delete_after_unzip --sourcepath src

```

## metadata template

### init apex class from template

```sh
sfdc meta:template:apex -d ./src -n HelloApex --template ApexClass.cls -v 47.0
sfdc meta:template:apex -d ./src -n HelloApexBatch --template BatchApexClass.cls -v 47.0
sfdc meta:template:apex -d ./src -n HelloApexTest --template UnitTestApexClass.cls -v 47.0
sfdc meta:template:apex -d ./src -n HelloApexBatchTest --template BDDUnitTestApexClass.cls -v 47.0
```

### init trigger from template

```sh
sfdc meta:template:trigger -d ./src -n HelloApexTrigger --sobject Opportunity --template ApexTrigger.trigger -v 47.0
sfdc meta:template:trigger -d ./src -n HelloApexTriggerAllEvents --sobject Opportunity --template ApexTriggerAllEvents.trigger -v 47.0
sfdc meta:template:trigger -d ./src -n HelloApexTriggerBulk --sobject Opportunity --template ApexTriggerBulk.trigger -v 47.0
```

### init visualforce from template

```sh
sfdc meta:template:page -d ./src -n HelloApexPage --template ApexPage.page -v 47.0
sfdc meta:template:page -d ./src -n HelloHeaderPageBlock --template HeaderPageBlock.page -v 47.0
```

### init visualforce component

```sh
sfdc meta:template:component -d ./src -n HelloCmp -v 47.0
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

## run apex testclass

```sh
sfdc test:run -p . -s ./src/classes/HelloApexTest.cls
sfdc test:run -p . -s ./src/classes/HelloApexBatchTest.cls
```

## get coverage

```sh
sfdc test:coverage -p . -f ./log/apex_coverage.log
```

## sobject

### list sobject

```sh
python3 -m sfdc_cli.cli sobject:list -p $project_dir
```

### export sobject as xlsx file

```sh
python3 -m sfdc_cli.cli sobject:xlsx -p $project_dir -s
```

## tools

### copy lightning

```sh
sfdc tools:copy:aura -f $from_lightning_path -t $to_lightning_path
sfdc tools:copy:aura -f /app/project/sfdc-project1/src/aura/HelloWorld -t /app/project/sfdc-project1/src/aura/HelloWorld1
```

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



# Acknowledgement

## Basic on OpenSource

1. [xlsxwriter (License: BSD)](https://github.com/jmcnamara/XlsxWriter)
2. [Simple-Salesforce (License: Apache 2.0)](https://pypi.python.org/pypi/simple-salesforce/0.72.2)
3. [requests (License: Apache 2.0)](https://pypi.python.org/pypi/requests/2.12.3)
4. [Apex Template From MavensMate](https://github.com/joeferraro/MavensMate/tree/master/app/lib/templates/github)