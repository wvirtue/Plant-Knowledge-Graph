# -*- coding: utf-8 -*-
import thulac
import csv
import sys
import os

from src.com.gzu.Model.mongo_model import Mongo
from src.com.gzu.Model.neo_models import Neo4j
from src.com.gzu.toolkit.tree_API import TREE
from src.com.gzu.toolkit.vec_API import word_vector_model

sys.path.append("..")

# from Model.neo_models import Neo4j
# from Model.mongo_model import Mongo
# from toolkit.vec_API import word_vector_model
# from toolkit.tree_API import TREE
pre_load_thu = thulac.thulac(user_dict='E:\学习\毕业论文文献及项目\项目\Plant_KnowledgeGraph\src\com\gzu\wikidataSpider\wikientities\iplant_entity.txt',seg_only=False)  #默认模式

# pre_load_thu = thulac.thulac()  #默认模式
print('thulac open!')

neo_con = Neo4j()   #预加载neo4j
neo_con.connectDB()
print('neo4j connected!')

predict_labels = {}   # 预加载实体到标注的映射字典
#filePath = os.getcwd()
filePath = 'E:\学习\毕业论文文献及项目\项目\Plant_KnowledgeGraph\src\com\gzu'
print(filePath)
# /wikidataSpider/wikientities/iplant_entityMark.txt
# /toolkit/predict_labels.txt
with open(filePath+'/wikidataSpider/wikientities/iplant_entityMark.txt','r',encoding="utf-8") as csvfile:
	reader = csv.reader(csvfile, delimiter=' ')
	for row in reader:
		predict_labels[str(row[0])] = int(row[1])
print('predicted labels load over!')

# 读取word vector
wv_model = word_vector_model()
#wv_model.read_vec('toolkit/vector_5.txt') # 测试用，节约读取时间
#wv_model.read_vec('toolkit/vector.txt')

wv_model.read_vec(filePath+'/toolkit/vector_15.txt') # 降到15维了	   

# 读取农业层次树
tree = TREE()
tree.read_edge(filePath+'/toolkit/plant_tree.txt')
tree.read_leaf(filePath+'/toolkit/leaf_list.txt')
		
print('level tree load over~~~')

		
# 预加载mongodb
mongo = Mongo()
mongo.makeConnection()
print("mongodb connected")
#连接数据库
mongodb = mongo.getDatabase("agricultureKnowledgeGraph")
print("connect to agricultureKnowledgeGraph")
# 得到collection
collection = mongo.getCollection("train_data")
print("get connection train_data")

testDataCollection = mongo.getCollection("test_data")
print("get connection test_data")