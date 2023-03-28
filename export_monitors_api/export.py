import json
import requests

# Export monitor json file
def exportFileRepo(json, id):
        with open(f"monitors_export/{id}.json", "w") as outfile:
            outfile.write(str(json))

#Export to readme.me file
def exportReadme(body):
    
    with open(f"readme.md", "w") as outfile:
        outfile.write(body)
        
#Building readme body and list services
def readmeBuilder(list):
    body        = ""
    bodyHeader  = "\n# Monitores Datadog Ame\nExport de todos os monitors do Datadog da Ame, para fins de backup.\n## Lista de Monitors\n"
    
    bodyList = ""
    for each in list:
        # print(each)
        bodyList += f"[Id:{str(each[0])}](https://github.com/user/repo/blob/branch/{str(each[0])}.json) {each[1]}\n"
   
    bodyFooter = "\n## Import Monitor\n Para fazer o import do serviço vá em [***Monitors > New Monitors > Import Monitor from JSON***](https://app.datadoghq.com/monitors/create/import) \n## Documentação\n[Documentação](https://docs.datadoghq.com/monitors/manage/status/#export-and-import)"
    body = ("%s %s %s"% (bodyHeader, bodyList, bodyFooter))
    
    exportReadme(body)
    
def callAllMonitorsDD():
    url = "https://api.datadoghq.com/api/v1/monitor"
    headers = {
        'Accept': 'application/json',
        'DD-API-KEY': {{'API_KEY'}},
        'DD-APPLICATION-KEY': {{'APP_KEY'}}
    }

    response = requests.get(url, headers=headers, data={}, timeout=30)
    print(response.status_code)
    
    if response.ok:
        return json.loads(response.text)
    else:
        exit(f"Execute:{response.text}")

def main():
    try:
        dataJson = callAllMonitorsDD()
    except Exception as err:
        print(err)
        
    export = {}
    listMonitors = []
        
    for data in dataJson:
            export['id']                    =     data['id']
            export['name']                  =     data['name']
            export['type']                  =     data['type']
            export['name']                  =     data['name']
            export['query']                 =     data['query']
            export['message']               =     data['message']
            export['tags']                  =     data['tags']
            export['options']               =     data['options']
            export['priority']              =     data['priority']
            export['restricted_roles']      =     data['restricted_roles']
            listMonitors.append([data['id'],data['name']])
            exportFileRepo(json.dumps(export,indent=4), data['id'])
            
    readmeBuilder(listMonitors)
        


if __name__ == main():
    main()