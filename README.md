# Plant Knowledge Graph

## 将import文件夹中的CSV文件导入Neo4j图数据库的步骤
### 导入植物品种节点
```
//将hudong_plant.csv导入neo4j
LOAD CSV WITH HEADERS  FROM "file:///hudong_plant.csv" AS line
CREATE (p:植物品种{title:line.title,image:line.image,detail:line.detail,url:line.url,openTypeList:line.openTypeList,baseInfoKeyList:line.baseInfoKeyList,baseInfoValueList:line.baseInfoValueList})
// 创建索引
CREATE CONSTRAINT ON (c:植物品种)
ASSERT c.title IS UNIQUE
```

### 导入植物产地节点
```
LOAD CSV WITH HEADERS FROM "file:///placeOfOriginNode.csv" AS line
CREATE (:植物产地 { title: line.placeOfOrigin })
```

### 创建植物产地索引
```
CREATE CONSTRAINT ON (c:植物产地)
ASSERT c.title IS UNIQUE
```

### 导入植物经济用途节点
```
LOAD CSV WITH HEADERS FROM "file:///func_node.csv" AS line
CREATE (:植物经济用途 { title: line.func })

//创建植物经济用途索引
CREATE CONSTRAINT ON (c:植物经济用途)
ASSERT c.title IS UNIQUE
```

### 创建经济用途实体到植物分类
```
LOAD CSV WITH HEADERS FROM "file:///plantClassify.csv" AS line
CREATE (:植物分类 { entity: line.entity })
```
### 导入新节点
```
// 导入互动百科抽取到的新节点
LOAD CSV WITH HEADERS FROM "file:///new_node.csv" AS line
CREATE (:NewNode { title: line.title })

// 导入维基百科抽取到的新节点
LOAD CSV WITH HEADERS FROM "file:///new_node_wiki.csv" AS line
CREATE (:NewNode { title: line.title })

//添加索引
CREATE CONSTRAINT ON (c:NewNode)
ASSERT c.title IS UNIQUE

//查询创建的索引
:schema
```

### 导入植物实体的关系和属性
```
//将attributes_p.csv放到neo4j的import目录下，然后执行
LOAD CSV WITH HEADERS FROM "file:///attributes_p.csv" AS line
MATCH (entity1:植物品种{title:line.Entity}), (entity2:植物品种{title:line.Attribute})
CREATE (entity1)-[:RELATION { type: line.AttributeName }]->(entity2);

LOAD CSV WITH HEADERS FROM "file:///attributes_p.csv" AS line
MATCH (entity1:植物品种{title:line.Entity}), (entity2:NewNode{title:line.Attribute})
CREATE (entity1)-[:RELATION { type: line.AttributeName }]->(entity2);


//将hudong_iplant_fusion.csv放到neo4j的import目录下，然后执行
LOAD CSV WITH HEADERS FROM "file:///hudong_iplant_fusion.csv" AS line
MATCH (entity1:植物品种{title:line.Entity}), (entity2:植物品种{title:line.Attribute})
CREATE (entity1)-[:RELATION { type: line.AttributeName }]->(entity2);

//将hudong_wiki_fusion.csv放到neo4j的import目录下，然后执行
LOAD CSV WITH HEADERS FROM "file:///hudong_wiki_fusion.csv" AS line
MATCH (entity1:植物品种{title:line.HudongItem1}), (entity2:植物品种{title:line.HudongItem2})
CREATE (entity1)-[:RELATION { type: line.relation }]->(entity2);

--导入植物产地关系
LOAD CSV WITH HEADERS FROM "file:///placeOfOrigin.csv" AS line
MATCH (entity1:植物品种{title:line.Entity}), (entity2:植物产地{title:line.Attribute})
CREATE (entity1)-[:RELATION { type: line.AttributeName }]->(entity2)

--导入经济用途、功用、治疗关系
LOAD CSV WITH HEADERS FROM "file:///iplantRelation.csv" AS line
MATCH (entity1:植物品种{title:line.iplantitem1}), (entity2:植物分类{entity:line.iplantitem2})
CREATE (entity1)-[:RELATION { type: line.relation }]->(entity2)

LOAD CSV WITH HEADERS FROM "file:///funcTriple.csv" AS line
MATCH (entity1:植物品种{title:line.entity}), (entity2:植物经济用途{title:line.value})
CREATE (entity1)-[:RELATION { type: line.relation }]->(entity2)

LOAD CSV WITH HEADERS FROM "file:///plant_func.csv" AS line
MATCH (entity1:植物品种{title:line.title}), (entity2:植物经济用途{title:line.value})
CREATE (entity1)-[:RELATION { type: line.relation }]->(entity2)

--导入iplantFunc
LOAD CSV FROM "file:///iplantFunc.csv" AS line
create (:iplantFunc{title:line[0]})
//添加索引
CREATE CONSTRAINT ON (c:iplantFunc)
ASSERT c.title IS UNIQUE

```
