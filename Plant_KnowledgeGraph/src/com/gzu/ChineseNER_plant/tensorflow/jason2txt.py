import json

def json2txt():
    with open("./hudong_plant.json","r",encoding='utf-8') as fr:
        with open("./plantname_dict.txt",'a',encoding='utf-8') as fwhudong:
            for line in fr:
                itemJson = json.loads(line)
                title = itemJson['title']
                for char in title:
                    if char >= u'\u4e00' and char <= u'\u9fa5':
                        fwhudong.write(char)
                    else:
                        continue
                fwhudong.write(' nz\n')
json2txt()