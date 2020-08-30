# 中国植物志植物位置数据转化为三元组
import json
import sys

if __name__ == "__main__":
    # if len(sys.argv) < 3:
    #     print("usage:python3 zhwiki.utf8.txt zhiwi.unseg.txt")
    #     exit(1)
    fout = open('E:\学习\毕业论文文献及项目\项目\Plant_KnowledgeGraph\src\com\gzu\wikidataSpider\wikidataAnalyse\plant_position_triple.csv', encoding='utf8', mode='w')
    fout.write("Entity,AttributeName,Attribute"+'\n')
    with open('E:\学习\毕业论文文献及项目\项目\Plant_KnowledgeGraph\src\com\gzu\wikidataSpider\wikidataAnalyse\plantposition.txt', encoding = 'utf8') as fin:
        for line in fin:
            # flag = False
            column = line.replace('\n','')
            if column == '--------------------':
                flag = True
                continue
            if flag:
                name = column
                flag = False
            if column.find('亚系')!=-1 and column.find('亚系') == len(column)-2:
                print(name+',亚系,'+column)
                fout.write(name+',亚系,'+column+'\n')
            elif column.find('系')!=-1 and column.find('系') == len(column)-1 and column.find('亚系')==-1:
                print(name+',系,'+column)
                fout.write(name+',系,'+column+'\n')
            elif column.find('亚组')!=-1 and column.find('亚组') == len(column)-2:
                print(name+',亚组,'+column)
                fout.write(name+',亚组,'+column+'\n')
            elif column.find('组')!=-1 and column.find('组') == len(column)-1 and column.find('亚组')==-1:
                print(name+',组,'+column)
                fout.write(name+',组,'+column+'\n')
            elif column.find('亚属')!=-1 and column.find('亚属') == len(column)-2:
                print(name+',亚属,'+column)
                fout.write(name+',亚属,'+column+'\n')
            elif column.find('属')!=-1 and column.find('属') == len(column)-1 and column.find('亚属')==-1:
                print(name+',属,'+column)
                fout.write(name+',属,'+column+'\n')
            elif column.find('亚族')!=-1 and column.find('亚族') == len(column)-2:
                print(name+',亚族,'+column)
                fout.write(name+',亚族,'+column+'\n')
            elif column.find('族')!=-1 and column.find('族') == len(column)-1 and column.find('亚族')==-1:
                print(name+',族,'+column)
                fout.write(name+',族,'+column+'\n')
            elif column.find('亚科')!=-1 and column.find('亚科') == len(column)-2:
                print(name+',亚科,'+column)
                fout.write(name+',亚科,'+column+'\n')
            elif column.find('科')!=-1 and column.find('科') == len(column)-1 and column.find('亚科')==-1:
                print(name+',科,'+column)
                fout.write(name+',科,'+column+'\n')
            elif column.find('亚目')!=-1 and column.find('亚目') == len(column)-2:
                print(name+',亚目,'+column)
                fout.write(name+',亚目,'+column+'\n')
            elif column.find('目')!=-1 and column.find('目') == len(column)-1 and column.find('亚目')==-1:
                print(name+',目,'+column)
                fout.write(name+',目,'+column+'\n')
            elif column.find('亚纲')!=-1 and column.find('亚纲') == len(column)-2:
                print(name+',亚纲,'+column)
                fout.write(name+',亚纲,'+column+'\n')
            elif column.find('纲')!=-1 and column.find('纲') == len(column)-1 and column.find('亚纲')==-1:
                print(name+',纲,'+column)
                fout.write(name+',纲,'+column+'\n')
            elif column.find('门')!=-1 and column.find('门') == len(column)-1:
                print(name+',门,'+column)
                fout.write(name+',门,'+column+'\n')