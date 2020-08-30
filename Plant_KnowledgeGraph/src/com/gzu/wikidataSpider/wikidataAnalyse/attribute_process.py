#属性关系去除科、目、纲等后面的英文
import csv
import sys
import re
import jieba.posseg as pseg

if __name__ == "__main__":

    def containenglish(str0):
        return bool(re.search('[a-z]', str0))

    fout = open('E:\学习\毕业论文文献及项目\项目\Plant_KnowledgeGraph\src\com\gzu\wikidataSpider\wikidataAnalyse\\attributes_p.csv', encoding='utf8', mode='w')
    fout.write("Entity,AttributeName,Attribute"+'\n')
    fout1 = open('E:\学习\毕业论文文献及项目\项目\Plant_KnowledgeGraph\src\com\gzu\wikidataSpider\wikidataAnalyse\\plant_placeOfOrigin.csv', encoding='utf8', mode='w')
    fout1.write("Entity,AttributeName,Attribute"+'\n')
    # f1 = open('E:\学习\毕业论文文献及项目\项目\Plant_KnowledgeGraph\src\com\gzu\wikidataSpider\wikidataAnalyse\\place_of_origin.csv', encoding='utf8', mode='w')
    # f1.write("Entity,place,placeValue"+'\n')
    nData = csv.reader(open('E:\学习\毕业论文文献及项目\项目\Plant_KnowledgeGraph\src\com\gzu\wikidataSpider\wikidataAnalyse\\attributes_plant.csv', encoding='utf8'),delimiter=',')
    pData = csv.reader(open('E:\学习\毕业论文文献及项目\项目\Plant_KnowledgeGraph\src\com\gzu\wikidataSpider\wikidataAnalyse\placeOfOrigin.csv', encoding='utf8'),delimiter=',')
    for line in nData:
        flag = False
        if line[0] == 'Entity':
            continue
        if line[1] == '门' or line[1] == '纲' or line[1] == '亚纲' or line[1] == '目' or line[1] == '亚目' or line[1] == '科' or line[1] == '亚科'\
                or line[1] == '族' or line[1] == '亚族' or line[1] == '属' or line[1] == '亚属' or line[1] == '组' or line[1] == '系':
            tail = ''
            if line[2].find('（')!=-1:
                fout.write(line[0]+','+line[1]+','+line[2].split('（')[0]+'\n')
            elif line[2].find('(')!=-1:
                fout.write(line[0]+','+line[1]+','+line[2].split('(')[0]+'\n')
            elif line[2].find(' ')!=-1:
                fout.write(line[0]+','+line[1]+','+line[2].split(' ')[0]+'\n')
            else:
                if containenglish(line[2]):
                    for t in line[2]:
                        if t >= u'\u4e00' and t <= u'\u9fa5':
                            tail += t
                    # print(tail)
                    if tail == '':
                        fout.write(line[0]+','+line[1]+','+line[2]+'\n')
                    else:
                        fout.write(line[0]+','+line[1]+','+tail+'\n')
                else:
                    fout.write(line[0]+','+line[1]+','+line[2]+'\n')
        elif line[1] == '分布区域':
            line_seg = "  ".join(['{0}/{1}'.format(w,t) for w,t in pseg.cut(line[2])])
            # print(line_seg)
            words = line_seg.split('  ')
            for id in words:
                tag = id[id.rfind('/')+1:]
                word = id[0:id.rfind('/')]
                if word == '模式':
                    break
                elif tag == 'ns' and len(word)>1:
                    # print(line[0]+','+line[1]+','+word)
                    fout1.write(line[0]+','+line[1]+','+word+'\n')
        elif line[1] == '界' or line[1] == '别名' or line[1] == '二名法' or line[1] == '拉丁学名' or line[1] == '亚界' or line[1] == '总门' or line[1] == '超目':
            fout.write(line[0]+','+line[1]+','+line[2]+'\n')

    for line1 in pData:
        line_seg = "  ".join(['{0}/{1}'.format(w,t) for w,t in pseg.cut(line1[2])])
        print(line_seg)
        words = line_seg.split('  ')
        for id in words:
            tag = id[id.rfind('/')+1:]
            word = id[0:id.rfind('/')]
            if tag == 'ns' and len(word)>1:
                print(line1[0]+','+line1[1]+','+word)
                fout1.write(line1[0]+','+line1[1]+','+word+'\n')