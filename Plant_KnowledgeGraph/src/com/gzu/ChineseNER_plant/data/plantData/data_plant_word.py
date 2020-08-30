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
    with open('E:\学习\深度学习相关\ChineseNER_plant\\tensorflow\plant_segwords.txt','r',encoding='utf-8') as inp,open('./plant2.txt','w', encoding='utf8',) as outp:
        for line in inp.readlines():
            line = line.split('  ')
            i = 0
            while i<len(line)-1:
                if line[i][0]=='[':
                    outp.write(line[i].split('/')[0][1:])
                    print(line[i].split('/')[0][1:])
                    i+=1
                    while i<len(line)-1 and line[i].find(']')==-1:
                        if line[i]!='':
                            outp.write(line[i].split('/')[0])
                            print(line[i].split('/')[0])
                        i+=1
                    outp.write(line[i].split('/')[0].strip()+'/'+line[i].split('/')[1][-2:]+' ')
                    print(line[i].split('/')[0].strip()+'/'+line[i].split('/')[1][-2:]+' ')
                elif line[i].split('/')[1]=='nr':
                    word = line[i].split('/')[0]
                    i+=1
                    if i<len(line)-1 and line[i].split('/')[1]=='nr':
                        outp.write(word+line[i].split('/')[0]+'/nr ')
                        print(word+line[i].split('/')[0]+'/nr ')
                    else:
                        outp.write(word+'/nr ')
                        print(word+'/nr ')
                        continue
                else:
                    outp.write(line[i]+' ')
                    print(line[i]+' ')
                i+=1
            outp.write('\n')
def originHandle2():
    with codecs.open('./plant2.txt','r', encoding='utf8',) as inp,codecs.open('./plant3.txt','w', encoding='utf8',) as outp:
        for line in inp.readlines():
            line = line.split(' ')
            i = 0
            while i<len(line)-1:
                if line[i]=='':
                    i+=1
                    continue
                word = line[i].split('/')[0]
                tag = line[i].split('/')[1]
                if tag=='nr' or tag=='ns' or tag=='nt' or tag=='nz':
                    outp.write(word[0]+"/B_"+tag+" ")
                    for j in word[1:len(word)-1]:
                        if j!=' ':
                            outp.write(j+"/M_"+tag+" ")
                    outp.write(word[-1]+"/E_"+tag+" ")
                else:
                    for wor in word:
                        outp.write(wor+'/O ')
                i+=1
            outp.write('\n')
def sentence2split():
    with open('./plant3.txt','r', encoding='utf8',) as inp,codecs.open('./plant4.txt','w','utf-8') as outp:
        texts = inp.read()
        sentences = re.split('[，。！？、‘’“”:]/[O]', texts)
        for sentence in sentences:
	        if sentence != " ":
		        outp.write(sentence.strip()+'\n')

def data2pkl():
    datas = list()
    labels = list()
    linedata=list()
    linelabel=list()
    tags = set()
    tags.add('')
    input_data = codecs.open('plant4.txt','r','utf-8')
    for line in input_data.readlines():
        line = line.split()
        linedata=[]
        linelabel=[]
        numNotO=0
        for word in line:
            word = word.split('/')
            linedata.append(word[0])
            linelabel.append(word[1])
            tags.add(word[1])
            if word[1]!='O':
                numNotO+=1
        if numNotO!=0:
            datas.append(linedata)
            labels.append(linelabel)

    input_data.close()
    print(len(datas))
    print(len(labels))
    all_words = flatten(datas)
    sr_allwords = pd.Series(all_words)
    sr_allwords = sr_allwords.value_counts()
    set_words = sr_allwords.index
    set_ids = range(1, len(set_words)+1)


    tags = [i for i in tags]
    tag_ids = range(len(tags))
    word2id = pd.Series(set_ids, index=set_words)
    id2word = pd.Series(set_words, index=set_ids)
    tag2id = pd.Series(tag_ids, index=tags)
    id2tag = pd.Series(tags, index=tag_ids)
    word2id["unknow"]=len(word2id)+1
    id2word[len(word2id)]="unknow"
    print(tag2id)
    max_len = 60
    def X_padding(words):
        ids = list(word2id[words])
        if len(ids) >= max_len:
            return ids[:max_len]
        ids.extend([0]*(max_len-len(ids)))
        return ids

    def y_padding(tags):
        ids = list(tag2id[tags])
        if len(ids) >= max_len:
            return ids[:max_len]
        ids.extend([0]*(max_len-len(ids)))
        return ids
    df_data = pd.DataFrame({'words': datas, 'tags': labels}, index=range(len(datas)))
    df_data['x'] = df_data['words'].apply(X_padding)
    df_data['y'] = df_data['tags'].apply(y_padding)
    x = np.asarray(list(df_data['x'].values))
    y = np.asarray(list(df_data['y'].values))

    from sklearn.model_selection import train_test_split
    x_train,x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=43)
    x_train, x_valid, y_train, y_valid = train_test_split(x_train, y_train,  test_size=0.2, random_state=43)


    import pickle
    import os
    with open('../plantdata.pkl', 'wb') as outp:
	    pickle.dump(word2id, outp)
	    pickle.dump(id2word, outp)
	    pickle.dump(tag2id, outp)
	    pickle.dump(id2tag, outp)
	    pickle.dump(x_train, outp)
	    pickle.dump(y_train, outp)
	    pickle.dump(x_test, outp)
	    pickle.dump(y_test, outp)
	    pickle.dump(x_valid, outp)
	    pickle.dump(y_valid, outp)
    print('** Finished saving the data.')



originHandle()
originHandle2()
sentence2split()
data2pkl()