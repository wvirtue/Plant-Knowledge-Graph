#互动百科导入新数据
import csv
import sys

from src.com.gzu.toolkit.pre_load import neo_con

if __name__ == "__main__":
    #连接数据库
    db = neo_con
    fout = open('F:\\Neo4j\\Neo4jData\\neo4jDatabases\\hudong_wiki_fusion.csv', encoding='utf8', mode='w')
    fout.write("HudongItem1,relation,HudongItem2"+'\n')
    nData = csv.reader(open('F:\\Neo4j\\Neo4jData\\neo4jDatabases\\wiki.csv', encoding='UTF-8-sig'),delimiter=',')
    for line in nData:
        flag = False
        if line[0] == 'HudongItem1':
            continue
        rel = db.findRelationByEntitys(line[0].replace("'",""),line[2].replace("'",""))
        if rel == []:
            fout.write(line[0]+','+line[1]+','+line[2]+'\n')
            print(line[0]+','+line[1]+','+line[2])
        else:
            print('data is exist:'+str(rel[0]["rel.type"]))