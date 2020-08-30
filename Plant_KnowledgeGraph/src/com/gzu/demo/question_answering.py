# -*- coding:utf-8 -*-
from django.shortcuts import render
from toolkit.pre_load import pre_load_thu
from toolkit.pre_load import neo_con
import random
import re

thu_lac = pre_load_thu
db = neo_con

def get_originPlace(obj,ret_dict):
	# nutrition = db.findOtherEntitiesmh(obj,"用")
	nutrition = db.findOtherEntitiescd(obj)
	if(len(nutrition) > 0 ):

		selected_index  = [i for i in range(len(nutrition))]

		for index in selected_index:

			y = nutrition[index]['rel']['type']
			if y == '分布区域':
				x = nutrition[index]['n2']['title']

			if(ret_dict.get('list') is  None):
				ret_dict['list'] = [{'entity1':obj,'rel':y,'entity2':x,'entity1_type':'主语','entity2_type':'元素'}]
			else:
				ret_dict['list'].append({'entity1':obj,'rel':y,'entity2':x,'entity1_type':'主语','entity2_type':'元素'})
			if(ret_dict.get('answer') is None):
				ret_dict['answer'] = [x]
			else:
				ret_dict['answer'].append(x)
	return ret_dict

def get_function(obj,ret_dict):
	# nutrition = db.findOtherEntitiesmh(obj,"用")
	nutrition = db.findOtherEntitiesgy(obj)
	if(len(nutrition) > 0 ):
		#结果数大于6则随机取6个
		if(len(nutrition) > 6):
			selected_index = []
			n = len(nutrition)
			m  = 6
			for i in range(n):
				rand = random.randint(0, n - i - 1)
				if(rand<m):
					m -= 1
					selected_index.append(i)
		else:
			selected_index  = [i for i in range(len(nutrition))]

		for index in selected_index:

			y = nutrition[index]['rel']['type']
			if y == '经济用途':
				x = nutrition[index]['n2']['entity']
			else:
				x = nutrition[index]['n2']['title']

			if(ret_dict.get('list') is  None):
				ret_dict['list'] = [{'entity1':obj,'rel':y,'entity2':x,'entity1_type':'主语','entity2_type':'元素'}]
			else:
				ret_dict['list'].append({'entity1':obj,'rel':y,'entity2':x,'entity1_type':'主语','entity2_type':'元素'})
			if y=='治疗':
				x = y+x
			if(ret_dict.get('answer') is None):
				ret_dict['answer'] = [x]
			else:
				ret_dict['answer'].append(x)
	return ret_dict

def get_plant_knowledge(obj,ret_dict):
	ke = db.findOtherEntities(obj,"科")
	if(len(ke) > 0 ):
		if(ret_dict.get('list') is None):
			ret_dict['list'] = [{'entity1':obj,'rel':'科','entity2':ke[0]['n2']['title'],'entity1_type':'植物','entity2_type':'类型'}]
		else:
			ret_dict['list'].append({'entity1': obj, 'rel': '科', 'entity2': ke[0]['n2']['title'],'entity1_type':'植物','entity2_type':'类型'})
		if(ret_dict.get('answer') is None):
			ret_dict['answer'] = [ke[0]['n2']['title']]
		else:
			ret_dict['answer'].append(ke[0]['n2']['title'])

	shu = db.findOtherEntities(obj,"属")
	if(len(shu) > 0 ):
		if(ret_dict.get('list') is None):
			ret_dict['list'] = [{'entity1':obj,'rel':'属','entity2':shu[0]['n2']['title'],'entity1_type':'植物','entity2_type':'类型'}]
		else:
			ret_dict['list'].append({'entity1': obj, 'rel': '属', 'entity2': shu[0]['n2']['title'],'entity1_type':'植物','entity2_type':'类型'})
		if (ret_dict.get('answer') is None):
			ret_dict['answer'] = [shu[0]['n2']['title']]
		else:
			ret_dict['answer'].append(shu[0]['n2']['title'])

	men = db.findOtherEntities(obj, "门")
	if (len(men) > 0):
		if (ret_dict.get('list') is None):
			ret_dict['list'] = [{'entity1': obj, 'rel': '门', 'entity2': men[0]['n2']['title'], 'entity1_type': '植物',
								 'entity2_type': '类型'}]
		else:
			ret_dict['list'].append({'entity1': obj, 'rel': '门', 'entity2': men[0]['n2']['title'], 'entity1_type': '植物',
									 'entity2_type': '类型'})
		if (ret_dict.get('answer') is None):
			ret_dict['answer'] = [men[0]['n2']['title']]
		else:
			ret_dict['answer'].append(men[0]['n2']['title'])

	gang = db.findOtherEntities(obj, "纲")
	if (len(gang) > 0):
		if (ret_dict.get('list') is None):
			ret_dict['list'] = [{'entity1': obj, 'rel': '纲', 'entity2': gang[0]['n2']['title'], 'entity1_type': '植物',
								 'entity2_type': '类型'}]
		else:
			ret_dict['list'].append({'entity1': obj, 'rel': '纲', 'entity2': gang[0]['n2']['title'], 'entity1_type': '植物',
									 'entity2_type': '类型'})
		if (ret_dict.get('answer') is None):
			ret_dict['answer'] = [gang[0]['n2']['title']]
		else:
			ret_dict['answer'].append(gang[0]['n2']['title'])

	mu = db.findOtherEntities(obj, "目")
	if (len(mu) > 0):
		if (ret_dict.get('list') is None):
			ret_dict['list'] = [{'entity1': obj, 'rel': '目', 'entity2': mu[0]['n2']['title'], 'entity1_type': '植物',
								 'entity2_type': '类型'}]
		else:
			ret_dict['list'].append({'entity1': obj, 'rel': '目', 'entity2': mu[0]['n2']['title'], 'entity1_type': '植物',
									 'entity2_type': '类型'})
		if (ret_dict.get('answer') is None):
			ret_dict['answer'] = [mu[0]['n2']['title']]
		else:
			ret_dict['answer'].append(mu[0]['n2']['title'])

	yamu = db.findOtherEntities(obj, "亚目")
	if (len(yamu) > 0):
		if (ret_dict.get('list') is None):
			ret_dict['list'] = [{'entity1': obj, 'rel': '亚目', 'entity2': yamu[0]['n2']['title'], 'entity1_type': '植物',
								 'entity2_type': '类型'}]
		else:
			ret_dict['list'].append({'entity1': obj, 'rel': '亚目', 'entity2': yamu[0]['n2']['title'], 'entity1_type': '植物',
									 'entity2_type': '类型'})
		if (ret_dict.get('answer') is None):
			ret_dict['answer'] = [yamu[0]['n2']['title']]
		else:
			ret_dict['answer'].append(yamu[0]['n2']['title'])

	yake = db.findOtherEntities(obj, "亚科")
	if (len(yake) > 0):
		if (ret_dict.get('list') is None):
			ret_dict['list'] = [{'entity1': obj, 'rel': '亚科', 'entity2': yake[0]['n2']['title'], 'entity1_type': '植物',
								 'entity2_type': '类型'}]
		else:
			ret_dict['list'].append(
				{'entity1': obj, 'rel': '亚科', 'entity2': yake[0]['n2']['title'], 'entity1_type': '植物',
				 'entity2_type': '类型'})
		if (ret_dict.get('answer') is None):
			ret_dict['answer'] = [yake[0]['n2']['title']]
		else:
			ret_dict['answer'].append(yake[0]['n2']['title'])

	return ret_dict

# pattern = [[r"适合种什么",r"种什么好"],
# 		   [r"气候是什么","气候类型是什么",r"属于哪种气候",r"是哪种气候",r"是什么天气",r"哪种天气",r"天气[\u4e00-\u9fa5]*"],
# 		   [r"有哪些营养",r"有[\u4e00-\u9fa5]+成分",r"含[\u4e00-\u9fa5]+成分",r"含[\u4e00-\u9fa5]+元素",r"有[\u4e00-\u9fa5]+营养",r"有[\u4e00-\u9fa5]+元素"],
# 		   [r"[\u4e00-\u9fa5]+植物学",r"[\u4e00-\u9fa5]+知识"]]
pattern = [[r"产地",r"分布区域"],
		   [r"气候是什么","气候类型是什么",r"属于哪种气候",r"是哪种气候",r"是什么天气",r"哪种天气",r"天气[\u4e00-\u9fa5]*"],
		   [r"有什么功用",r"有[\u4e00-\u9fa5]+功用",r"含[\u4e00-\u9fa5]+功用",r"有什么经济用途",r"有[\u4e00-\u9fa5]+经济用途",r"含[\u4e00-\u9fa5]+经济用途"],
		   [r"[\u4e00-\u9fa5]+植物学",r"[\u4e00-\u9fa5]+知识"]]
def question_answering(request):  # index页面需要一开始就加载的内容写在这里
	context = {'ctx':''}
	if(request.GET):
		question = request.GET['question']
		cut_statement = thu_lac.cut(question,text=False)
		print(cut_statement)
		address_name = []
		weather_name = []
		question_name = ""
		ret_dict = {}

		pos = -1
		q_type  = -1
		for i in range(len(pattern)):
			for x in pattern[i]:
				index  =  re.search(x,question)
				if(index):
					pos = index.span()[0]
					q_type= i
					break
			if(pos!=-1):
				break

		print(pos)
		#匹配问题 xxx植物的产地
		zhuyu = ""
		if(q_type==0):
			index = 0
			for x in cut_statement:
				if(index > pos):
					break
				index += len(x)
				if x[1] == 'uw':
					zhuyu = x[0]

			if(len(zhuyu)>0):
				ret_dict = get_originPlace(zhuyu,ret_dict)

		##匹配问题：属于哪种气候
		if(q_type == 1):
			print()

		#匹配问题，植物有什么功用
		zhuyu = ""
		if(q_type == 2):
			index = 0
			for x in cut_statement:
				if(index > pos):
					break
				index += len(x)
				if(x[1] == 'n' or x[1] == 'uw'):
					zhuyu = zhuyu+x[0]

			if(len(zhuyu)>0):
				ret_dict = get_function(zhuyu,ret_dict)

		#匹配问题，植物学知识
		zhuyu = ""
		if(q_type == 3):
			index = 0
			for x in cut_statement:
				if(index>pos):
					break
				index += len(x)
				if(x[1] == 'n' or x[1] == 'uw'):
					zhuyu =  zhuyu+x[0]

			if(len(zhuyu)>0):
				ret_dict = get_plant_knowledge(zhuyu,ret_dict)

		print(ret_dict)

		if(len(ret_dict)!=0  and ret_dict!=0):
			return render(request,'question_answering.html',{'ret':ret_dict})
		print(context)
		return render(request, 'question_answering.html', {'ctx':'暂未找到答案'})
	return render(request, 'question_answering.html', context)