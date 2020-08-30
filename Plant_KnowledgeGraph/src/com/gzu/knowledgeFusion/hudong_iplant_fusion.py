#互动百科与植物志的关系融合
import csv
import sys

from src.com.gzu.toolkit.pre_load import neo_con

if __name__ == "__main__":
    #连接数据库
    db = neo_con
    fout = open('F:\\Neo4j\\Neo4jData\\neo4jDatabases\\hudong_iplant_fusion.csv', encoding='utf8', mode='w')
    fout.write("Entity,AttributeName,Attribute"+'\n')
    nData = csv.reader(open('E:\学习\毕业论文文献及项目\项目\Plant_KnowledgeGraph\src\com\gzu\wikidataSpider\wikidataAnalyse\plant_position_triple.csv', encoding='utf8'),delimiter=',')
    for line in nData:
        flag = False
        if line[0] == 'Entity':
            continue
        tail = db.findEntitiesByHeadAndRel(line[0].replace("'",""),line[1].replace("'",""))
        if tail == [] or line[2].replace("'","")!=str(tail[0]["n2.title"]):
            fout.write(line[0]+','+line[1]+','+line[2]+'\n')
            print(line[0]+','+line[1]+','+line[2])
        else:
            print('data is exist:'+str(tail[0]["n2.title"]))