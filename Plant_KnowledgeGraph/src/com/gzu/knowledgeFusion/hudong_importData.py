#互动百科导入新数据
import csv
import sys

from src.com.gzu.toolkit.pre_load import neo_con

if __name__ == "__main__":
    #连接数据库
    db = neo_con
    fout = open('F:\\Neo4j\\Neo4jData\\neo4jDatabases\\hudong_newData.csv', encoding='utf8', mode='w')
    fout.write("title,url,image,openTypeList,detail,baseInfoKeyList,baseInfoValueList"+'\n')
    # nData = csv.reader(open('C://Users//wangyq//Documents//Neo4j//default.graphdb//import//wike.csv', encoding='utf8'),delimiter=',')
    with open('E:\学习\毕业论文文献及项目\项目\Plant_KnowledgeGraph\src\com\gzu\wikidataSpider\wikientities\plantName.txt', encoding = 'utf8') as fin:
        for line in fin:
            flag = False
            line = line.replace('\n','')
            result = db.newMatchHudongItembyTitle(line)
            if result == []:
                fout.write(line+',,,,,,'+'\n')
                print(line+',,,,,,')
            else:
                print('data is exist:'+str(result[0]["n.title"]))