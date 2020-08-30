# -*- coding: UTF-8 -*-

import codecs
import re
import pdb
import pandas as pd
import numpy as np
import collections
import jieba.posseg as pseg

from nltk import flatten

def originHandle():
    dic = ['花冠','种翅','一回羽片','2回羽片','末回裂片','花','花瓣','萼片','花萼','花柄','花药','花丝','雄蕊','子房','胚珠','雄花',
           '雌花','花柱','雌蕊','苞片','瘦果','种子','蒴果','叶','叶片','叶脉','花梗','花葶','蓇葖','叶序','总状花序','果实',
           '裂片','根茎','柱头','果梗','孢子','退化雌蕊','退化雄蕊','叶鞘','托叶','种皮','胚','胚乳','根','茎','叶膜','果',
           '头状果序','头状花序','花序','总状伞形花序','花序梗','复伞形花序','花粉团','雄球花','总苞片','小总苞片','伞花序']
    dicSeq = ['互生','对生','轮生','簇生','单生','顶生','侧生','直立']
    dicB = ['干后','上部','下部','基部','中下部','下半部','上面','下面']
    disease_dic = []
    with open('E:\学习\毕业论文文献及项目\项目\KnowledgeGraph_Agriculture-master\Plants\disease_dic.txt',encoding='UTF-8-sig') as fin:
        for line in fin.readlines():
            disease_dic.append(line.split(' ')[0])
    with open('./test_segwords.txt','r',encoding='utf8') as inp,open('./plant_test.txt','w', encoding='utf8',) as outp:
        for line in inp.readlines():
            line = line.split('  ')
            sen = ''
            psplit = []
            i = 0
            k = 0

            for t in range(len(line)):
                words = line[t][0:line[t].rfind('/')]
                sen +=words
            seg = sen.split('，')
            for s in seg:
                psplit.append(s)
            senS = psplit[k]
            flagN = None
            while i<len(line):
                flagO = True
                seqName = ''
                # ss =line[i].rfind('/')
                # print(line[i][0:ss])
                # wordw = line[i][0,]
                # word = line[i].split('/')[0]
                # tag = line[i].split('/')[1]

                word = line[i][0:line[i].rfind('/')]
                tag = line[i][line[i].rfind('/')+1:]
                if tag == 'x' and word == '，' and k < len(line)-1:
                    k +=1
                    senS = psplit[k]
                f = re.findall(r'[^\*"/:?\\|()（）<>]',senS)
                g = "".join(f)
                for sequence in dicSeq:
                    if word == sequence:
                        seqName = word
                for be in dicB:
                    if word == be:
                        flagO = False
                        if len(word) == 1:
                            outp.write(word[0]+"/S_Organ_part ")
                            print(word[0]+"/S_Organ_part ")
                        else:
                            outp.write(word[0]+"/B_Organ_part ")
                            print(word[0]+"/B_Organ_part ")
                            for j in word[1:len(word)-1]:
                                if j!=' ':
                                    outp.write(j+"/M_Organ_part ")
                                    print(j+"/M_Organ_part ")
                            outp.write(word[-1]+"/E_Organ_part ")
                            print(word[-1]+"/E_Organ_part ")
                        i += 1
                for head in dic:
                    if word == head:
                        nameN =word
                        if len(word) == 1:
                            outp.write(word[0]+"/S_Organ ")
                            print(word[0]+"/S_Organ ")
                        else:
                            outp.write(word[0]+"/B_Organ ")
                            print(word[0]+"/B_Organ ")
                            for j in word[1:len(word)-1]:
                                if j!=' ':
                                    outp.write(j+"/M_Organ ")
                                    print(j+"/M_Organ ")
                            outp.write(word[-1]+"/E_Organ ")
                            print(word[-1]+"/E_Organ ")
                        i += 1
                        flagO = False
                        flagN =re.search(r'{}\d'.format(nameN),g)

                if i == 0:
                    if len(word) == 1:
                        outp.write(word[0]+"/S_pName ")
                        print(word[0]+"/S_pName ")
                    else:
                        outp.write(word[0]+"/B_pName ")
                        print(word[0]+"/B_pName ")
                        for j in word[1:len(word)-1]:
                            if j!=' ':
                                outp.write(j+"/M_pName ")
                                print(j+"/M_pName ")
                        outp.write(word[-1]+"/E_pName ")
                        print(word[-1]+"/E_pName ")
                    flagO = False
                    i += 1
                elif '草本' in word or '年生' in word or '乔木' in word or '灌木' in word:
                    if len(word) == 1:
                        outp.write(word[0]+"/S_Life_form ")
                        print(word[0]+"/S_Life_form ")
                    else:
                        outp.write(word[0]+"/B_Life_form ")
                        print(word[0]+"/B_Life_form ")
                        for j in word[1:len(word)-1]:
                            if j!=' ':
                                outp.write(j+"/M_Life_form ")
                                print(j+"/M_Life_form ")
                        outp.write(word[-1]+"/E_Life_form ")
                        print(word[-1]+"/E_Life_form ")
                    flagO = False
                    i += 1
                elif '质' in word and word != '质' and word != '质地' and word != '蛋白质':
                    if len(word) == 1:
                        outp.write(word[0]+"/S_Texture ")
                        print(word[0]+"/S_Texture ")
                    else:
                        outp.write(word[0]+"/B_Texture ")
                        print(word[0]+"/B_Texture ")
                        for j in word[1:len(word)-1]:
                            if j!=' ':
                                outp.write(j+"/M_Texture ")
                                print(j+"/M_Texture ")
                        outp.write(word[-1]+"/E_Texture ")
                        print(word[-1]+"/E_Texture ")
                    flagO = False
                    i += 1
                elif '形' in word and '形成' not in word:
                    if len(word) == 1:
                        outp.write(word[0]+"/S_Shape ")
                        print(word[0]+"/S_Shape ")
                    else:
                        outp.write(word[0]+"/B_Shape ")
                        print(word[0]+"/B_Shape ")
                        for j in word[1:len(word)-1]:
                            if j!=' ':
                                outp.write(j+"/M_Shape ")
                                print(j+"/M_Shape ")
                        outp.write(word[-1]+"/E_Shape ")
                        print(word[-1]+"/E_Shape ")
                    flagO = False
                    i += 1
                elif '色' in word and '毛' not in word :
                    if len(word) == 1:
                        outp.write(word[0]+"/S_Color ")
                        print(word[0]+"/S_Color ")
                    else:
                        outp.write(word[0]+"/B_Color ")
                        print(word[0]+"/B_Color ")
                        for j in word[1:len(word)-1]:
                            if j!=' ':
                                outp.write(j+"/M_Color ")
                                print(j+"/M_Color ")
                        outp.write(word[-1]+"/E_Color ")
                        print(word[-1]+"/E_Color ")
                    flagO = False
                    i += 1
                elif (('宽' in word or '长' in word or '高' in word or '直径' in word or '径' in word) and '米' in senS) or word =='产' or \
                        word == '产于' or word == '特产' or word == '生于' or word =='模式标本' or word =='海拔':
                    if len(word) == 1:
                        outp.write(word[0]+"/S_Property ")
                        print(word[0]+"/S_Property ")
                    else:
                        outp.write(word[0]+"/B_Property ")
                        print(word[0]+"/B_Property ")
                        for j in word[1:len(word)-1]:
                            if j!=' ':
                                outp.write(j+"/M_Property ")
                                print(j+"/M_Property ")
                        outp.write(word[-1]+"/E_Property ")
                        print(word[-1]+"/E_Property ")
                    flagO = False
                    i += 1
                pro = ('宽' in senS or '长' in senS or '高' in senS or '直径' in senS or '径' in senS ) and '米' in senS
                tex = '质' in senS and senS != '质' and senS != '质地' and senS != '蛋白质'
                if tex:
                    if '约' in word or '达' in word or '近' in word:
                        outp.write(word[0]+"/S_Degree ")
                        print(word[0]+"/S_Degree ")
                        flagO = False
                        i += 1
                if  pro:
                    if '约' in word or '达' in word or '近' in word:
                        outp.write(word[0]+"/S_Degree ")
                        print(word[0]+"/S_Degree ")
                        flagO = False
                        i += 1
                try:
                    flag =re.search(r'{}+至'.format(word),senS)
                    flag1 = re.search(r'至+{}'.format(word),senS)
                    flag2 = re.search(r'(\d+(\.\d+)?)+厘米|毫米|米|月',senS)
                    flag3 = re.search(r'\d+(\.\d+)?',word)
                except:
                    print(line)
                if (pro and '至' in senS and flag and flag3) or (flagN and flag3 and flag and '至' in senS):
                    if len(word) == 1:
                        outp.write(word[0]+"/S_MinValue ")
                        print(word[0]+"/S_MinValue ")
                    else:
                        outp.write(word[0]+"/B_MinValue ")
                        print(word[0]+"/B_MinValue ")
                        for j in word[1:len(word)-1]:
                            if j!=' ':
                                outp.write(j+"/M_MinValue ")
                                print(j+"/M_MinValue ")
                        outp.write(word[-1]+"/E_MinValue ")
                        print(word[-1]+"/E_MinValue ")
                    flagO = False
                    flag1 = None
                    i += 1
                if (pro and '至' in senS and flag1 and flag3) or (flagN and flag3 and flag1 and '至' in senS):
                    if len(word) == 1:
                        outp.write(word[0]+"/S_MaxValue ")
                        print(word[0]+"/S_MaxValue ")
                    else:
                        outp.write(word[0]+"/B_MaxValue ")
                        print(word[0]+"/B_MaxValue ")
                        for j in word[1:len(word)-1]:
                            if j!=' ':
                                outp.write(j+"/M_MaxValue ")
                                print(j+"/M_MaxValue ")
                        outp.write(word[-1]+"/E_MaxValue ")
                        print(word[-1]+"/E_MaxValue ")
                    flagO = False
                    i += 1
                if ('至' not in senS and flag2 and flag3) or ('至' not in senS and flagN and flag3):
                    if len(word) == 1:
                        outp.write(word[0]+"/S_ProValue ")
                        print(word[0]+"/S_ProValue ")
                    else:
                        outp.write(word[0]+"/B_ProValue ")
                        print(word[0]+"/B_ProValue ")
                        for j in word[1:len(word)-1]:
                            if j!=' ':
                                outp.write(j+"/M_ProValue ")
                                print(j+"/M_ProValue ")
                        outp.write(word[-1]+"/E_ProValue ")
                        print(word[-1]+"/E_ProValue ")
                    flagO = False
                    i += 1
                if ('米' in word or '月' in word) and flag2:
                    if len(word) == 1:
                        outp.write(word[0]+"/S_Unit ")
                        print(word[0]+"/S_Unit ")
                    else:
                        outp.write(word[0]+"/B_Unit ")
                        print(word[0]+"/B_Unit ")
                        for j in word[1:len(word)-1]:
                            if j!=' ':
                                outp.write(j+"/M_Unit ")
                                print(j+"/M_Unit ")
                        outp.write(word[-1]+"/E_Unit ")
                        print(word[-1]+"/E_Unit ")
                    flagO = False
                    i += 1
                        # if '至' in word:
                        #     outp.write(word[0]+"/O_Degree ")
                        #     i += 1
                elif seqName != '':
                    if len(word) == 1:
                        outp.write(word[0]+"/S_Growth_form ")
                        print(word[0]+"/S_Growth_form ")
                    else:
                        outp.write(word[0]+"/B_Growth_form ")
                        print(word[0]+"/B_Growth_form ")
                        for j in word[1:len(word)-1]:
                            if j!=' ':
                                outp.write(j+"/M_Growth_form ")
                                print(j+"/M_Growth_form ")
                        outp.write(word[-1]+"/E_Growth_form ")
                        print(word[-1]+"/E_Growth_form ")
                    flagO = False
                    i += 1
                elif '花期' in word or '果期' in word or '花果期' in word or '开花' in word or '笋期' in word:
                    if len(word) == 1:
                        outp.write(word[0]+"/S_Period ")
                        print(word[0]+"/S_Period ")
                    else:
                        outp.write(word[0]+"/B_Period ")
                        print(word[0]+"/B_Period ")
                        for j in word[1:len(word)-1]:
                            if j!=' ':
                                outp.write(j+"/M_Period ")
                                print(j+"/M_Period ")
                        outp.write(word[-1]+"/E_Period ")
                        print(word[-1]+"/E_Period ")
                    flagO = False
                    i += 1
                # origin = '产' in senS or '产于' in senS or '特产' in senS
                elif ('产' in senS or '生于' in senS or '产于' in senS or '特产' in senS or '模式标本' in senS) and tag == 'ns':
                    if len(word) == 1:
                        outp.write(word[0]+"/S_Place_of_origin ")
                        print(word[0]+"/S_Place_of_origin ")
                    else:
                        outp.write(word[0]+"/B_Place_of_origin ")
                        print(word[0]+"/B_Place_of_origin ")
                        for j in word[1:len(word)-1]:
                            if j!=' ':
                                outp.write(j+"/M_Place_of_origin ")
                                print(j+"/M_Place_of_origin ")
                        outp.write(word[-1]+"/E_Place_of_origin ")
                        print(word[-1]+"/E_Place_of_origin ")
                    flagO = False
                    i += 1
                elif flagO:
                    if len(word) == 1:
                        outp.write(word+'/S ')
                        print(word+'/S ')
                    else:
                        outp.write(word+'/O ')
                        print(word+'/O ')
                    i+=1
            outp.write('\n')



originHandle()
#                 if line[i][0]=='[':
#                     outp.write(line[i].split('/')[0][1:])
#                     print(line[i].split('/')[0][1:])
#                     i+=1
#                     while i<len(line)-1 and line[i].find(']')==-1:
#                         if line[i]!='':
#                             outp.write(line[i].split('/')[0])
#                             print(line[i].split('/')[0])
#                         i+=1
#                     outp.write(line[i].split('/')[0].strip()+'/'+line[i].split('/')[1][-2:]+' ')
#                     print(line[i].split('/')[0].strip()+'/'+line[i].split('/')[1][-2:]+' ')
#                 elif line[i].split('/')[1]=='nr':
#                     word = line[i].split('/')[0]
#                     i+=1
#                     if i<len(line)-1 and line[i].split('/')[1]=='nr':
#                         outp.write(word+line[i].split('/')[0]+'/nr ')
#                         print(word+line[i].split('/')[0]+'/nr ')
#                     else:
#                         outp.write(word+'/nr ')
#                         print(word+'/nr ')
#                         continue
#                 else:
#                     outp.write(line[i]+' ')
#                     print(line[i]+' ')
#                 i+=1
#             outp.write('\n')
# def originHandle2():
#     with codecs.open('./plant2.txt','r', encoding='utf8',) as inp,codecs.open('./plant3.txt','w', encoding='utf8',) as outp:
#         for line in inp.readlines():
#             line = line.split(' ')
#             i = 0
#             while i<len(line)-1:
#                 if line[i]=='':
#                     i+=1
#                     continue
#                 word = line[i].split('/')[0]
#                 tag = line[i].split('/')[1]
#                 if tag=='nr' or tag=='ns' or tag=='nt' or tag=='nz':
#                     outp.write(word[0]+"/B_"+tag+" ")
#                     for j in word[1:len(word)-1]:
#                         if j!=' ':
#                             outp.write(j+"/M_"+tag+" ")
#                     outp.write(word[-1]+"/E_"+tag+" ")
#                 else:
#                     for wor in word:
#                         outp.write(wor+'/O ')
#                 i+=1
#             outp.write('\n')
# def sentence2split():
#     with open('./plant3.txt','r', encoding='utf8',) as inp,codecs.open('./plant4.txt','w','utf-8') as outp:
#         texts = inp.read()
#         sentences = re.split('[，。！？、‘’“”:]/[O]', texts)
#         for sentence in sentences:
# 	        if sentence != " ":
# 		        outp.write(sentence.strip())
#
# def data2pkl():
#     datas = list()
#     labels = list()
#     linedata=list()
#     linelabel=list()
#     tags = set()
#     tags.add('')
#     input_data = codecs.open('plant2.txt','r','utf-8')
#     for line in input_data.readlines():
#         line = line.split()
#         linedata=[]
#         linelabel=[]
#         numNotO=0
#         for word in line:
#             word = word.split('/')
#             linedata.append(word[0])
#             linelabel.append(word[1])
#             tags.add(word[1])
#             if word[1]!='O':
#                 numNotO+=1
#         if numNotO!=0:
#             datas.append(linedata)
#             labels.append(linelabel)
#
#     input_data.close()
#     print(len(datas))
#     print(len(labels))
#     all_words = flatten(datas)
#     sr_allwords = pd.Series(all_words)
#     sr_allwords = sr_allwords.value_counts()
#     set_words = sr_allwords.index
#     set_ids = range(1, len(set_words)+1)
#
#
#     tags = [i for i in tags]
#     tag_ids = range(len(tags))
#     word2id = pd.Series(set_ids, index=set_words)
#     id2word = pd.Series(set_words, index=set_ids)
#     tag2id = pd.Series(tag_ids, index=tags)
#     id2tag = pd.Series(tags, index=tag_ids)
#     word2id["unknow"]=len(word2id)+1
#     id2word[len(word2id)]="unknow"
#     print(tag2id)
#     max_len = 60
#     def X_padding(words):
#         ids = list(word2id[words])
#         if len(ids) >= max_len:
#             return ids[:max_len]
#         ids.extend([0]*(max_len-len(ids)))
#         return ids
#
#     def y_padding(tags):
#         ids = list(tag2id[tags])
#         if len(ids) >= max_len:
#             return ids[:max_len]
#         ids.extend([0]*(max_len-len(ids)))
#         return ids
#     df_data = pd.DataFrame({'words': datas, 'tags': labels}, index=range(len(datas)))
#     df_data['x'] = df_data['words'].apply(X_padding)
#     df_data['y'] = df_data['tags'].apply(y_padding)
#     x = np.asarray(list(df_data['x'].values))
#     y = np.asarray(list(df_data['y'].values))
#
#     from sklearn.model_selection import train_test_split
#     x_train,x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=43)
#     x_train, x_valid, y_train, y_valid = train_test_split(x_train, y_train,  test_size=0.2, random_state=43)
#
#
#     import pickle
#     import os
#     with open('../plantdata.pkl', 'wb') as outp:
# 	    pickle.dump(word2id, outp)
# 	    pickle.dump(id2word, outp)
# 	    pickle.dump(tag2id, outp)
# 	    pickle.dump(id2tag, outp)
# 	    pickle.dump(x_train, outp)
# 	    pickle.dump(y_train, outp)
# 	    pickle.dump(x_test, outp)
# 	    pickle.dump(y_test, outp)
# 	    pickle.dump(x_valid, outp)
# 	    pickle.dump(y_valid, outp)
#     print('** Finished saving the data.')

#
#
# originHandle()
# originHandle2()
# sentence2split()
# data2pkl()