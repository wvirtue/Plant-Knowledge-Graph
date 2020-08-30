from py2neo import Graph, Node, Relationship, cypher, Path
import neo4j
class Neo4j():
	graph = None
	def __init__(self):
		print("create neo4j class ...")

	def connectDB(self):
		self.graph = Graph("http://localhost:11004/", username="neo4j", password="111")

	def matchItembyTitle(self,value):
		sql = "MATCH (n:Item { title: '" + str(value) + "' }) return n;"
		answer = self.graph.run(sql).data()
		return answer

	# 根据title值返回互动百科item
	def matchHudongItembyTitle(self,value):
		sql = "MATCH (n:植物品种 { title: '" + str(value) + "' }) return n;"
		answer = self.graph.run(sql).data()
		print(answer)
		return answer
	# 根据title值返回互动百科item
	def newMatchHudongItembyTitle(self,value):
		sql = "MATCH (n:植物品种 { title: '" + str(value) + "' }) return n.title;"
		answer = self.graph.run(sql).data()
		print(answer)
		return answer
	# 根据title值返回新节点item
	def MatchNewNodeItembyTitle(self,value):
		sql = "MATCH (n:NewNode { title: '" + str(value) + "' }) return n.title;"
		answer = self.graph.run(sql).data()
		# print(answer)
		return answer
	#根据entity1和关系查找enitty2
	def findEntitiesByHeadAndRel(self,entity,relation):
		answer = self.graph.run("MATCH (n1 {title:\"" + str(entity) + "\"})- [rel {type:\""+str(relation)+"\"}] -> (n2) RETURN n2.title" ).data()
		print(answer)
		return answer

	# 根据entity的名称返回关系
	def getEntityRelationbyEntity(self,value):
		answer = self.graph.run("MATCH (entity1) - [rel] -> (entity2)  WHERE entity1.title = \"" +str(value)+"\" RETURN rel,entity2").data()
		print(answer)
		return answer

	#根据头尾实体查找其对应的关系
	def findRelationByEntitys(self,entity1,entity2):
		answer = self.graph.run("MATCH (n1 {title:\""+str(entity1)+"\"})- [rel] -> (n2 {title:\""+str(entity2)+"\"}) RETURN rel.type" ).data()
		# if(answer is None):
		# 	answer = self.graph.run("MATCH (n1:NewNode {title:\""+entity1+"\"})- [rel] -> (n2) RETURN n1,rel,n2" ).data()
		print(answer)
		return answer

	#查找entity1及其对应的关系（与getEntityRelationbyEntity的差别就是返回值不一样）
	def findRelationByEntity(self,entity1):
		answer = self.graph.run("MATCH (n1 {title:\""+str(entity1)+"\"})- [rel] -> (n2) RETURN n1,rel,n2" ).data()
		# if(answer is None):
		# 	answer = self.graph.run("MATCH (n1:NewNode {title:\""+entity1+"\"})- [rel] -> (n2) RETURN n1,rel,n2" ).data()
		print(answer)
		return answer

	#查找entity2及其对应的关系
	def findRelationByEntity2(self,entity1):
		answer = self.graph.run("MATCH (n1)- [rel] -> (n2 {title:\""+str(entity1)+"\"}) RETURN n1,rel,n2" ).data()
		print(answer)
		# if(answer is None):
		# 	answer = self.graph.run("MATCH (n1)- [rel] -> (n2:NewNode {title:\""+entity1+"\"}) RETURN n1,rel,n2" ).data()
		return answer

	#根据entity1和关系查找enitty2
	def findOtherEntities(self,entity,relation):
		answer = self.graph.run("MATCH (n1 {title:\"" + str(entity) + "\"})- [rel {type:\""+str(relation)+"\"}] -> (n2) RETURN n1,rel,n2" ).data()
		#if(answer is None):
		#	answer = self.graph.run("MATCH (n1:NewNode {title:\"" + entity + "\"})- [rel:RELATION {type:\""+relation+"\"}] -> (n2) RETURN n1,rel,n2" ).data()
		print(answer)
		return answer
	#MATCH (n1 {title:'高乌头'})- [rel] -> (n2) where rel.type =~'.*用.*' RETURN n1,rel,n2
	def findOtherEntitiesmh(self,entity,relation):
		answer = self.graph.run("MATCH (n1 {title:\"" + str(entity) + "\"})- [rel] -> (n2) WHERE rel.type=~'.*"+str(relation)+".*' RETURN n1,rel,n2" ).data()
		#if(answer is None):
		#	answer = self.graph.run("MATCH (n1:NewNode {title:\"" + entity + "\"})- [rel:RELATION {type:\""+relation+"\"}] -> (n2) RETURN n1,rel,n2" ).data()
		print("MATCH (n1 {title:\"" + str(entity) + "\"})- [rel] -> (n2) WHERE rel.type=~'.*"+str(relation)+".*' RETURN n1,rel,n2")
		print(answer)
		return answer
	def findOtherEntitiesgy(self,entity):
		answer1 = self.graph.run("MATCH (n1 {title:\"" + str(entity) + "\"})- [rel] -> (n2:植物经济用途) RETURN n1,rel,n2" ).data()
		answer2 = self.graph.run("MATCH (n1 {title:\"" + str(entity) + "\"})- [rel] -> (n2:植物分类) RETURN n1,rel,n2" ).data()
		answer = answer1+answer2
		print("MATCH (n1 {title:\"" + str(entity) + "\"})- [rel] -> (n2:植物经济用途) RETURN n1,rel,n2")
		print(answer)
		return answer

	def findOtherEntitiescd(self,entity):
		answer = self.graph.run("MATCH (n1 {title:\"" + str(entity) + "\"})- [rel] -> (n2:植物产地) RETURN n1,rel,n2" ).data()
		print("MATCH (n1 {title:\"" + str(entity) + "\"})- [rel] -> (n2:植物产地) RETURN n1,rel,n2")
		print(answer)
		return answer

	#根据entity2和关系查找enitty1
	def findOtherEntities2(self,entity,relation):
		answer = self.graph.run("MATCH (n1)- [rel {type:\""+str(relation)+"\"}] -> (n2 {title:\"" + str(entity) + "\"}) RETURN n1,rel,n2" ).data()
		#if(answer is None):
		#	answer = self.graph.run("MATCH (n1)- [rel:RELATION {type:\""+relation+"\"}] -> (n2:NewNode {title:\"" + entity + "\"}) RETURN n1,rel,n2" ).data()
		print(answer)
		return answer

	#根据两个实体查询它们之间的最短路径
	def findRelationByEntities(self,entity1,entity2):
		answer = self.graph.run("MATCH (p1:植物品种 {title:\"" + str(entity1) + "\"}),(p2:植物品种{title:\""+str(entity2)+"\"}),p=shortestpath((p1)-[rel:RELATION*]-(p2)) RETURN rel").evaluate()
		#answer = self.graph.run("MATCH (p1:植物品种 {title:\"" + entity1 + "\"})-[rel:RELATION]-(p2:植物品种{title:\""+entity2+"\"}) RETURN p1,p2").data()
		
		if(answer is None):	
			answer = self.graph.run("MATCH (p1:植物品种 {title:\"" + str(entity1) + "\"}),(p2:NewNode {title:\""+str(entity2)+"\"}),p=shortestpath((p1)-[rel:RELATION*]-(p2)) RETURN p").evaluate()
		if(answer is None):
			answer = self.graph.run("MATCH (p1:NewNode {title:\"" + str(entity1) + "\"}),(p2:植物品种{title:\""+str(entity2)+"\"}),p=shortestpath((p1)-[rel:RELATION*]-(p2)) RETURN p").evaluate()
		if(answer is None):
			answer = self.graph.run("MATCH (p1:NewNode {title:\"" + str(entity1) + "\"}),(p2:NewNode {title:\""+str(entity2)+"\"}),p=shortestpath((p1)-[rel:RELATION*]-(p2)) RETURN p").evaluate()
		#answer = self.graph.data("MATCH (n1:植物品种 {title:\"" + entity1 + "\"})- [rel] -> (n2:植物品种{title:\""+entity2+"\"}) RETURN n1,rel,n2" )
		#if(answer is None):
		#	answer = self.graph.data("MATCH (n1:植物品种 {title:\"" + entity1 + "\"})- [rel] -> (n2:NewNode{title:\""+entity2+"\"}) RETURN n1,rel,n2" )
		#if(answer is None):
		#	answer = self.graph.data("MATCH (n1:NewNode {title:\"" + entity1 + "\"})- [rel] -> (n2:植物品种{title:\""+entity2+"\"}) RETURN n1,rel,n2" )
		#if(answer is None):
		#	answer = self.graph.data("MATCH (n1:NewNode {title:\"" + entity1 + "\"})- [rel] -> (n2:NewNode{title:\""+entity2+"\"}) RETURN n1,rel,n2" )
		relationDict = []
		if(answer is not None):
			for x in answer:
				tmp = {}
				start_node = x.start_node
				end_node = x.end_node
				tmp['n1'] = start_node
				tmp['n2'] = end_node
				tmp['rel'] = x
				relationDict.append(tmp)		
		return relationDict

	#查询数据库中是否有对应的实体-关系匹配
	def findEntityRelation(self,entity1,relation,entity2):
		answer = self.graph.run("MATCH (n1:植物品种 {title:\"" + str(entity1) + "\"})- [rel:RELATION {type:\""+str(relation)+"\"}] -> (n2:植物品种{title:\""+entity2+"\"}) RETURN n1,rel,n2" ).data()
		if(answer is None):
			answer = self.graph.run("MATCH (n1:植物品种 {title:\"" + str(entity1) + "\"})- [rel:RELATION {type:\""+str(relation)+"\"}] -> (n2:NewNode{title:\""+entity2+"\"}) RETURN n1,rel,n2" ).data()
		if(answer is None):
			answer = self.graph.run("MATCH (n1:NewNode {title:\"" + str(entity1) + "\"})- [rel:RELATION {type:\""+str(relation)+"\"}] -> (n2:植物品种{title:\""+entity2+"\"}) RETURN n1,rel,n2" ).data()
		if(answer is None):
			answer = self.graph.run("MATCH (n1:NewNode {title:\"" + str(entity1) + "\"})- [rel:RELATION {type:\""+str(relation)+"\"}] -> (n2:NewNode{title:\""+entity2+"\"}) RETURN n1,rel,n2" ).data()
		print(answer)
		return answer

