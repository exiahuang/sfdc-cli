# Usage

## print help

```sh
sfdc -h
```

## new project

```sh
sfdc project:init -d project/sfdc-project1
```

## metadata retrieve

```sh
# retrieve zip file of all metadata
sfdc meta:retrieve -p project/sfdc-project1 -d project/package -n package.zip

# retrieve zip file of choice metadata : ApexClass ApexTrigger ApexPage
sfdc meta:retrieve -p project/sfdc-project1 -d project/package -n package1.zip -m ApexClass ApexTrigger ApexPage ApexComponent CustomObject

# retrieve metadata and unzip, source path: src
sfdc meta:retrieve -p project/sfdc-project1 -d project/package -n package2.zip -m ApexClass ApexTrigger ApexPage AuraDefinitionBundle LightningComponentBundle --unzip --delete_after_unzip --sourcepath src

```

## metadata template

### init apex class from template

```sh
sfdc meta:template:apex -d project/sfdc-project1/src -n HelloApex --template ApexClass.cls -v 47.0
sfdc meta:template:apex -d project/sfdc-project1/src -n HelloApexBatch --template BatchApexClass.cls -v 47.0
sfdc meta:template:apex -d project/sfdc-project1/src -n HelloApexTest --template UnitTestApexClass.cls -v 47.0
sfdc meta:template:apex -d project/sfdc-project1/src -n HelloApexBatchTest --template BDDUnitTestApexClass.cls -v 47.0
```

### init trigger from template

```sh
sfdc meta:template:trigger -d project/sfdc-project1/src -n HelloApexTrigger --sobject Opportunity --template ApexTrigger.trigger -v 47.0
sfdc meta:template:trigger -d project/sfdc-project1/src -n HelloApexTriggerAllEvents --sobject Opportunity --template ApexTriggerAllEvents.trigger -v 47.0
sfdc meta:template:trigger -d project/sfdc-project1/src -n HelloApexTriggerBulk --sobject Opportunity --template ApexTriggerBulk.trigger -v 47.0
```

### init visualforce from template

```sh
sfdc meta:template:page -d project/sfdc-project1/src -n HelloApexPage --template ApexPage.page -v 47.0
sfdc meta:template:page -d project/sfdc-project1/src -n HelloHeaderPageBlock --template HeaderPageBlock.page -v 47.0
```

### init visualforce component

```sh
sfdc meta:template:component -d project/sfdc-project1/src -n HelloCmp -v 47.0
```

## metadata new/update/refresh/delete

### new metadata

```sh
sfdc meta:new -p project/sfdc-project1 -s project/sfdc-project1/src/classes/HelloApex.cls
sfdc meta:new -p project/sfdc-project1 -s project/sfdc-project1/src/classes/HelloApexBatch.cls
sfdc meta:new -p project/sfdc-project1 -s project/sfdc-project1/src/classes/HelloApexTest.cls
sfdc meta:new -p project/sfdc-project1 -s project/sfdc-project1/src/classes/HelloApexBatchTest.cls
sfdc meta:new -p project/sfdc-project1 -s project/sfdc-project1/src/pages/HelloApexPage.page
sfdc meta:new -p project/sfdc-project1 -s project/sfdc-project1/src/components/HelloCmp.component
sfdc meta:new -p project/sfdc-project1 -s project/sfdc-project1/src/triggers/HelloApexTrigger.trigger --sobject Opportunity
sfdc meta:new -p project/sfdc-project1 -s project/sfdc-project1/src/triggers/HelloApexTriggerAllEvents.trigger --sobject Opportunity
sfdc meta:new -p project/sfdc-project1 -s project/sfdc-project1/src/triggers/HelloApexTriggerBulk.trigger --sobject Opportunity
```

### update metadata

```sh
sfdc meta:update -p project/sfdc-project1 -s project/sfdc-project1/src/classes/HelloApex.cls
sfdc meta:update -p project/sfdc-project1 -s project/sfdc-project1/src/classes/HelloApexBatch.cls
sfdc meta:update -p project/sfdc-project1 -s project/sfdc-project1/src/classes/HelloApexTest.cls
sfdc meta:update -p project/sfdc-project1 -s project/sfdc-project1/src/classes/HelloApexBatchTest.cls
sfdc meta:update -p project/sfdc-project1 -s project/sfdc-project1/src/pages/HelloApexPage.page
sfdc meta:update -p project/sfdc-project1 -s project/sfdc-project1/src/components/HelloCmp.component
sfdc meta:update -p project/sfdc-project1 -s project/sfdc-project1/src/triggers/HelloApexTrigger.trigger
sfdc meta:update -p project/sfdc-project1 -s project/sfdc-project1/src/triggers/HelloApexTriggerAllEvents.trigger
sfdc meta:update -p project/sfdc-project1 -s project/sfdc-project1/src/triggers/HelloApexTriggerBulk.trigger
```

### metadata refresh

#### metadata refresh by filepath

```sh
# refresh apex/trigger/page/copmonent/ aura file
sfdc meta:refresh -p . -s src/classes/HelloApex.cls
sfdc meta:refresh -p project/sfdc-project1 -s project/sfdc-project1/src/classes/HelloApex.cls
sfdc meta:refresh -p project/sfdc-project1 -s project/sfdc-project1/src/classes/HelloApexBatch.cls
sfdc meta:refresh -p project/sfdc-project1 -s project/sfdc-project1/src/aura/HelloWorld/HelloWorld.cmp
sfdc meta:refresh -p project/sfdc-project1 -s project/sfdc-project1/src/aura/HelloWorld/HelloWorld.css
sfdc meta:refresh -p project/sfdc-project1 -s project/sfdc-project1/src/aura/HelloWorld
```

#### metadata refresh by directory

```sh

# refresh directory, examples
sfdc meta:refresh:dir -p project/sfdc-project1 -d project/sfdc-project1/src/classes
sfdc meta:refresh:dir -p project/sfdc-project1 -d project/sfdc-project1/src/triggers
sfdc meta:refresh:dir -p project/sfdc-project1 -d project/sfdc-project1/src/components
sfdc meta:refresh:dir -p project/sfdc-project1 -d project/sfdc-project1/src/pages
sfdc meta:refresh:dir -p project/sfdc-project1 -d project/sfdc-project1/src/layouts
sfdc meta:refresh:dir -p project/sfdc-project1 -d project/sfdc-project1/src/lwc
sfdc meta:refresh:dir -p project/sfdc-project1 -d project/sfdc-project1/src/aura

# refresh one aura componet
sfdc meta:refresh:aura -p project/sfdc-project1 -s project/sfdc-project1/src/aura/HelloWorld

```

### delete metadata

```sh
sfdc meta:delete -p project/sfdc-project1 -s project/sfdc-project1/src/classes/HelloApex.cls
sfdc meta:delete -p project/sfdc-project1 -s project/sfdc-project1/src/classes/HelloApexBatch.cls
sfdc meta:delete -p project/sfdc-project1 -s project/sfdc-project1/src/classes/HelloApexTest.cls
sfdc meta:delete -p project/sfdc-project1 -s project/sfdc-project1/src/classes/HelloApexBatchTest.cls
sfdc meta:delete -p project/sfdc-project1 -s project/sfdc-project1/src/pages/HelloApexPage.page
sfdc meta:delete -p project/sfdc-project1 -s project/sfdc-project1/src/components/HelloCmp.component
sfdc meta:delete -p project/sfdc-project1 -s project/sfdc-project1/src/triggers/HelloApexTrigger.trigger
```

## metadata attribute

```sh
sfdc meta:attr -p project/sfdc-project1 -s project/sfdc-project1/src/classes/HelloApex.cls
```

## package.xml

### build from server

```sh
# build package in current directory, filename package.xml
sfdc packagexml:server

sfdc packagexml:server -p project/sfdc-project1 -d project/sfdc-project1 -n package.xml
```

### build from local

scan directory and build package.xml

```sh
sfdc packagexml:local --scandir project/sfdc-project1/src --savedir project/sfdc-project1 -n package.xml
```

## run apex testclass

```sh
sfdc test:run -p project/sfdc-project1 -s project/sfdc-project1/src/classes/HelloApexTest.cls
sfdc test:run -p project/sfdc-project1 -s project/sfdc-project1/src/classes/HelloApexBatchTest.cls
```

## get coverage

```sh
sfdc test:coverage -p project/sfdc-project1 -f project/sfdc-project1/log/apex_coverage.log
```
