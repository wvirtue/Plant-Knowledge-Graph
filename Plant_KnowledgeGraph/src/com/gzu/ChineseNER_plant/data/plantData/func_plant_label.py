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
    with open('./func_segwords.txt','r',encoding='utf8') as inp,open('./plant_func.txt','w', encoding='utf8',) as outp:
        for line in inp.readlines():
            line = line.split('  ')
            sen = ''
            psplit = []
            i = 0
            k = 0

            # for t in range(len(line)):
            #     words = line[t][0:line[t].rfind('/')]
            #     sen +=words
            # seg = sen.split('，')
            # for s in seg:
            #     psplit.append(s)
            # senS = psplit[k]
            # flagN = None
            while i<len(line):
                flagO = True
                seqName = ''
                # ss =line[i].rfind('/')
                # print(line[i][0:ss])
                # wordw = line[i][0,]
                # word = line[i].split('/')[0]
                # tag = line[i].split('/')[1]

                word = line[i][0:line[i].rfind('/')]
                # tag = line[i][line[i].rfind('/')+1:]
                # if tag == 'x' and word == '，' and k < len(line)-1:
                #     k +=1
                #     senS = psplit[k]
                # f = re.findall(r'[^\*"/:?\\|()（）<>]',senS)
                # g = "".join(f)
                # for sequence in dicSeq:
                #     if word == sequence:
                #         seqName = word
                for dise in disease_dic:
                    if dise == word:
                        if len(word) == 1:
                            outp.write(word[0]+"/S_Disease ")
                            print(word[0]+"/S_Disease ")
                        else:
                            outp.write(word[0]+"/B_Disease ")
                            print(word[0]+"/B_Disease ")
                            for j in word[1:len(word)-1]:
                                if j!=' ':
                                    outp.write(j+"/M_Disease ")
                                    print(j+"/M_Disease ")
                            outp.write(word[-1]+"/E_Disease ")
                            print(word[-1]+"/E_Disease ")
                        flagO = False
                        i += 1
                # if i == 0:
                #     if len(word) == 1:
                #         outp.write(word[0]+"/S_pName ")
                #         print(word[0]+"/S_pName ")
                #     else:
                #         outp.write(word[0]+"/B_pName ")
                #         print(word[0]+"/B_pName ")
                #         for j in word[1:len(word)-1]:
                #             if j!=' ':
                #                 outp.write(j+"/M_pName ")
                #                 print(j+"/M_pName ")
                #         outp.write(word[-1]+"/E_pName ")
                #         print(word[-1]+"/E_pName ")
                #     flagO = False
                #     i += 1
                if flagO:
                    # if len(word) == 1:
                    #     outp.write(word+'/S ')
                    #     print(word+'/S ')
                    # else:
                    outp.write(word+'/O ')
                    print(word+'/O ')
                    i+=1
            outp.write('\n')
def sentence2split():
    with open('./plant_func.txt','r', encoding='utf8',) as inp,codecs.open('./plant_function.txt','w','utf-8') as outp:
        texts = inp.read()
        sentences = re.split('[，。！？、‘’“”:；]/[O]', texts)
        for sentence in sentences:
            if sentence != " ":
                outp.write(sentence.strip()+'\n')
originHandle()
sentence2split()