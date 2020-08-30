#查询数据库，新导入数据不在hudongItem实体节点中，则加入NewNode
import csv
import sys

from src.com.gzu.toolkit.pre_load import neo_con

if __name__ == "__main__":
    #连接数据库
    # db = neo_con
    # fout = open('F:\\Neo4j\\Neo4jData\\neo4jDatabases\\database-1b35b01a-5019-468b-8704-01b334440d45\\installation-4.1.0\\import\\new_node_wiki.csv', encoding='utf-8', mode='w')
    # fout.write("title,label"+'\n')
    # nData = csv.reader(open('F:\\Neo4j\\Neo4jData\\neo4jDatabases\\hudong_wiki_fusion.csv', encoding='utf-8'),delimiter=',')
    # for line in nData:
    #     # fout.write(line[2]+',newNode'+'\n')
    #     if line[0] == 'Entity':
    #         continue
    #     result = db.newMatchHudongItembyTitle(line[2].replace("'",""))
    #     if result == []:
    #         fout.write(line[2]+',newNode'+'\n')
    #         print(line[2]+',newNode')
    #     else:
    #         print('data is exist:'+str(result[0]["n.title"]))

    db = neo_con
    fout = open('F:\\Neo4j\\Neo4jData\\neo4jDatabases\\database-1b35b01a-5019-468b-8704-01b334440d45\\installation-4.1.0\\import\\new_node.csv', encoding='utf-8', mode='w')
    fout.write("title,label"+'\n')
    nData = csv.reader(open('F:\\Neo4j\\Neo4jData\\neo4jDatabases\\database-1b35b01a-5019-468b-8704-01b334440d45\\installation-4.1.0\\import\\new_node1.csv', encoding='UTF-8-sig'),delimiter=',')
    for line in nData:
        # fout.write(line[2]+',newNode'+'\n')
        if line[0] == 'title':
            continue
        result = db.newMatchHudongItembyTitle(line[0].replace("'",""))
        if result == []:
            fout.write(line[0]+',newNode'+'\n')
            print(line[0]+',newNode')
        else:
            print('data is exist:'+str(result[0]["n.title"]))