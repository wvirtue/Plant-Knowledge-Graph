#互动百科和维基百科植物知识融合
import csv
import sys
import difflib

import Levenshtein

print(Levenshtein.ratio('被子植物门', '被子植物门tewerwe'))
from difflib import SequenceMatcher
def similarity(a, b):
     return SequenceMatcher(None, a, b).ratio()

print(similarity('被子植物门', '被子植物门tewerwe'))

def similar(str1, str2):
    str1 = str1 + ' ' * (len(str2) - len(str1))
    str2 = str2 + ' ' * (len(str1) - len(str2))
    return sum(1 if i == j else 0
               for i, j in zip(str1, str2)) / float(len(str1))


print (similar('被子植物门', '被子植物门tewerwe'))
# from src.com.gzu.toolkit.pre_load import neo_con
#
# if __name__ == "__main__":
#     #连接数据库
#     db = neo_con
#     fout = open('C://Users//wangyq//Documents//Neo4j//default.graphdb//import//tripleFusion.csv', encoding='utf8', mode='w')
#     fout.write("title,label"+'\n')
#     nData = csv.reader(open('C://Users//wangyq//Documents//Neo4j//default.graphdb//import//wike.csv', encoding='utf8'),delimiter=',')
#     for line in nData:
#         flag = False
#         if line[0] == 'Entity1':
#             continue
#         result = db.newMatchHudongItembyTitle(line[0].replace("'",""))
#         if result == []:
#             fout.write(line[0]+',newNode'+'\n')
#             print(line[0]+',newNode')
#         else:
#             print('data is exist:'+str(result[0]["n.title"]))