#NewNode去掉与Hudong_pedia相同的实体
import csv
import sys

from src.com.gzu.toolkit.pre_load import neo_con

if __name__ == "__main__":
    #连接数据库
    db = neo_con
    fout = open('F:\\Neo4j\\Neo4jData\\neo4jDatabases\\database-1b35b01a-5019-468b-8704-01b334440d45\\installation-4.1.0\\import\\new_node_wiki.csv', encoding='utf-8', mode='w')
    fout.write("title,label"+'\n')
    nData = csv.reader(open('F:\\Neo4j\\Neo4jData\\neo4jDatabases\\new_node_wiki.csv', encoding='utf-8'),delimiter=',')
    for line in nData:
        # flag = False
        # if line[0] == 'Entity1':
        if line[0] == 'title':
            continue
        # result = db.newMatchHudongItembyTitle(line[0].replace("'",""))
        result = db.MatchNewNodeItembyTitle(line[0].replace("'",""))
        result1 = db.newMatchHudongItembyTitle(line[0].replace("'",""))
        if result == [] and result1 == []:
            fout.write(line[0]+',newNode'+'\n')
            print(line[0]+',newNode')
        else:
            # print('data is exist:'+str(result[0]["n.title"]))
            print('data is exist')