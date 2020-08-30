import json

def json2csv():
    with open("./data/hudong_pedia.csv",'w',encoding='utf-8') as fw:
        fw.write("title$url$image$openTypeList$detail$baseInfoKeyList$baseInfoValueList"+'\n')
    with open("./data/hudong_plant.json","r",encoding='utf-8') as fr:
        with open("./data/hudong_pedia.csv",'a',encoding='utf-8') as fwhudong:
            for line in fr:
                itemJson = json.loads(line)
                title = itemJson['title']
                url = itemJson['url']
                image = itemJson['image']
                openTypeList = itemJson['openTypeList']
                detail = itemJson['detail']
                baseInfoKeyList = itemJson['baseInfoKeyList']
                baseInfoValueList = itemJson['baseInfoValueList']
                fwhudong.write(title+"$"+url+"$"+image+"$"+openTypeList+"$"+detail+"$"+baseInfoKeyList+"$"+baseInfoValueList+'\n')

json2csv()