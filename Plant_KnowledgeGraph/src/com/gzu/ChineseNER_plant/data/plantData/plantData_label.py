# -*- coding: utf-8 -*-
import os
import re
from pyltp import SentenceSplitter, Segmentor, NamedEntityRecognizer, Postagger
import csv

import jieba
import pandas as pd
import jieba.posseg as pseg

LTP_DATA_DIR='E:/ltp_data_v3.4.0'
cws_model_path = os.path.join(LTP_DATA_DIR, 'cws.model')  # 分词模型路径，模型名称为`cws.model`
pos_model_path = os.path.join(LTP_DATA_DIR, 'pos.model')  # 词性标注模型路径，模型名称为`pos.model`
ner_model_path = os.path.join(LTP_DATA_DIR, 'ner.model')  # 命名实体识别模型路径，模型名称为`ner.model`
par_model_path = os.path.join(LTP_DATA_DIR, 'parser.model')	 # 依存句法分析模型路径，模型名称为`parser.model`

# 分词
def segmentorF(sentence):
    segmentor = Segmentor()	 # 初始化实例
    # segmentor.load(cws_model_path)	# 加载模型
    segmentor.load_with_lexicon(cws_model_path, 'E:/iplant_entity.txt') #加载模型	  使用用户自定义字典的高级分词
    words = segmentor.segment(sentence)	 # 分词
    # 默认可以这样输出
    #print('/'.join(words))
    # 可以转换成List 输出
    words_list = list(words)
    segmentor.release()	 # 释放模型
    return words_list
#创建停用词表
def stopwordslist(filepath):
    stopwords = [line.strip() for line in open(filepath, 'r', encoding='utf-8').readlines()]
    return stopwords
def e_recognize(words, postags):
    recognizer = NamedEntityRecognizer()  # 初始化实例
    recognizer.load(ner_model_path)	 # 加载模型
    netags = recognizer.recognize(words, postags)  # 命名实体识别
    #for word, ntag in zip(words, netags):
    #print(word + '/' + ntag)
    recognizer.release()  # 释放模型
    return netags
# 词性标注
def posttagger(words):
    postagger = Postagger()	 # 初始化实例
    postagger.load(pos_model_path)	# 加载模型
    postags = postagger.postag(words)  # 词性标注
    #for word, tag in zip(words, postags):
    #print(word + '/' + tag)
    postagger.release()	 # 释放模型
    return postags
#利用LTP实现对输入的.csv文件的分句、分词、词性标注、命名实体识别和三元组抽取
def myltp(input_path, output_path):
    records = pd.read_csv(input_path,error_bad_lines=False)
    # csv.reader(open(input_path, encoding='UTF-8-sig'),delimiter=',')
    f = open(input_path,encoding='utf-8')

    titles = records['title']
    openTypeLists = records['openTypeList']
    details = records['detail']
    # stopwords = stopwordslist('E:\学习\毕业论文文献及项目\项目\KnowledgeGraph_Agriculture-master\stopwords\中文停用词表.txt')
    # f1 = open('E:\学习\毕业论文文献及项目\项目\KnowledgeGraph_Agriculture-master\Plants\plantTxt\\train\\plant_train.csv', encoding='utf8', mode='w')
    # f2 = open('E:\学习\毕业论文文献及项目\项目\KnowledgeGraph_Agriculture-master\Plants\plantTxt\\train\\other.csv', encoding='utf8', mode='w')
    # f3 = open('E:\学习\毕业论文文献及项目\项目\KnowledgeGraph_Agriculture-master\Plants\plantTxt\\train\\trainTriple2.txt', encoding='utf8', mode='w')
    # f1 = open('E:\学习\毕业论文文献及项目\项目\KnowledgeGraph_Agriculture-master\Plants\plantTxt\lifeForm.txt', encoding='utf8', mode='w')
    # f2 = open('E:\学习\毕业论文文献及项目\项目\KnowledgeGraph_Agriculture-master\Plants\plantTxt\\flowerPeriod.txt', encoding='utf8', mode='w')
    # f3 = open('E:\学习\毕业论文文献及项目\项目\KnowledgeGraph_Agriculture-master\Plants\plantTxt\\altitude.txt', encoding='utf8', mode='w')
    # f4 = open('E:\学习\毕业论文文献及项目\项目\KnowledgeGraph_Agriculture-master\Plants\plantTxt\\placeOfOrigin.txt', encoding='utf8', mode='w')
    # f5 = open('E:\学习\毕业论文文献及项目\项目\KnowledgeGraph_Agriculture-master\Plants\plantTxt\\typeSpecimen.txt', encoding='utf8', mode='w')
    # f6 = open('E:\学习\毕业论文文献及项目\项目\KnowledgeGraph_Agriculture-master\Plants\plantTxt\\function.txt', encoding='utf8', mode='w')
    # f7 = open('E:\学习\毕业论文文献及项目\项目\KnowledgeGraph_Agriculture-master\Plants\plantTxt\\喙长.csv', encoding='utf8', mode='w')
    # f1 = open('E:\学习\毕业论文文献及项目\项目\KnowledgeGraph_Agriculture-master\Plants\plantTxt\\train\\flower.csv', encoding='utf8', mode='w')
    # f1.write("title,openTypeList,detail"+'\n')
    f1 = open('E:\学习\毕业论文文献及项目\项目\KnowledgeGraph_Agriculture-master\Plants\plantTxt\\train\\plant_train.txt', encoding='utf8', mode='w')
    f2 = open('E:\学习\毕业论文文献及项目\项目\KnowledgeGraph_Agriculture-master\Plants\plantTxt\\train\\plant_word2vec.txt', encoding='utf8', mode='w')
    f3 = open('E:\学习\毕业论文文献及项目\项目\KnowledgeGraph_Agriculture-master\Plants\plantTxt\\train\\plant_testify.txt', encoding='utf8', mode='w')
    f4 = open('E:\学习\毕业论文文献及项目\项目\KnowledgeGraph_Agriculture-master\Plants\plantTxt\\train\\plant_triple.csv', encoding='utf8', mode='w')
    f5 = open('E:\学习\毕业论文文献及项目\项目\KnowledgeGraph_Agriculture-master\Plants\plantTxt\\train\\plant_dic.txt', encoding='utf8', mode='w')
    # f1.write("title,openTypeList,detail"+'\n')
    # f8 = open('E:\学习\毕业论文文献及项目\项目\KnowledgeGraph_Agriculture-master\Plants\plantTxt\\exFlowerTriple.csv', encoding='utf8', mode='w')
    # f8.write("title,openTypeList,detail"+'\n')
    #405282 153837 163252
    for i in range(163252):
        # for i in range(1):
        # print(i)
        #分句
        # sents = SentenceSplitter.split(details[i])
        #
        # sent = '\n{title}'.join(sents)
        # sentF = sent.format(title=titles[i])
        sentM = details[i]
        # for sentM in sentF.split('\n'):
        # flag1 =re.search(r'\d+月',sentM, flags=0)
        flag =re.search(r'\d+毫米|厘米|米',sentM, flags=0)

        if titles[i] != None and type(titles[i]) is str:
            f2.write(sentM+'\n')
            sentO = sentM.replace(titles[i],'')
            jieba.load_userdict('E:\学习\毕业论文文献及项目\项目\KnowledgeGraph_Agriculture-master\Plants\iplant_dic.txt')
            sent_cut = jieba.lcut(sentO)

            dic = ['花冠','种翅','一回羽片','2回羽片','末回裂片','花','花瓣','萼片','花萼','花柄','花药','花丝','雄蕊','子房','胚珠','雄花',
                   '雌花','花柱','雌蕊','苞片','瘦果','种子','蒴果','叶','叶片','叶脉','花梗','花葶','蓇葖','叶序','总状花序','果实',
                   '裂片','根茎','柱头','果梗','孢子','退化雌蕊','退化雄蕊','叶鞘','托叶','种皮','胚','胚乳','根','茎','叶膜','果',
                   '头状果序','总状伞形花序','花序梗','复伞形花序','花粉团','雄球花','总苞片','小总苞片','伞花序']
            dicSeq = ['互生','对生','轮生','簇生','单生','顶生','侧生']
            dicB = ['干后','上部','下部','基部','中下部','下半部','上面','下面']
            # dicB = []
            # flagA = False
            # for head in dic:
            #     if sent_cut[0] == head:
            #         flagA = True
            #
            # if flagA:
            #     f1.write(titles[i]+',植物,'+sentM+'\n')
            # else:
            #     f2.write(titles[i]+',植物,'+sentM+'\n')
            # print(flagN)
            # if '花' in sentO  or '萼' in sentO or '子房' in sentO or '胚珠' in sentO or '花瓣' in sentO or '雌蕊' in sentO:
            #     f1.write(titles[i]+',植物,'+sentM+'\n')
            if sentO.find('花瓣')==0:
                if '形，长' in sentO  and flag and '长、宽' not in sentO:

                    nameN = sent_cut[0]
                    for id in sentO.split('，'):
                        partFlag = False
                        seqName = ''
                        id_cuts = jieba.lcut(id)
                        f = re.findall(r'[^\*"/:?\\|()（）<>]',id)
                        g = "".join(f)
                        flagN =re.search(r'{}\d'.format(nameN),g)
                        flagJ =re.search(r'{}\d'.format('径'),id)
                        name = nameN
                        for id_cut in id_cuts:
                            if '质' in id_cut:
                                tail =id_cut

                            for head in dic:
                                if id_cut == head:
                                    nameN =id_cut
                                    flagN =re.search(r'{}\d'.format(nameN),g)
                            name1 = nameN
                            # name = nameN
                            for be in dicB:
                                if id_cut == be:
                                    nameP = id_cut
                                    # name = nameN + id_cut
                                    part = id_cut
                                    partFlag = True
                            for sequence in dicSeq:
                                if id_cut == sequence:
                                    seqName = id_cut
                        if partFlag == False:
                            name = nameN

                        if seqName != '':
                            f1.write(seqName[0]+"/B_Growth_form ")
                            print(seqName[0]+"/B_Growth_form ")
                            for j in seqName[1:len(seqName)-1]:
                                if j!=' ':
                                    f1.write(j+"/M_Growth_form ")
                                    print(j+"/M_Growth_form ")
                            f1.write(seqName[-1]+"/E_Growth_form ")
                            print(seqName[-1]+"/E_Growth_form ")
                            # f1.write(name + '\t' +seqName+'\t'+'has_growth_form'+' '+sentM+'\n')
                            # f4.write(titles[i] +',has_organ,'+name+'\n')
                            # f4.write(name+',has_growth_form,'+seqName+'\n')
                            # f4.write(titles[i]+','+name+'生长型,'+seqName+'\n')
                        if '质' in id and tail != '质' and tail != '质地' and tail != '蛋白质':
                            f1.write(tail[0]+"/B_Texture ")
                            print(tail[0]+"/B_Texture ")
                            for j in tail[1:len(tail)-1]:
                                if j!=' ':
                                    f1.write(j+"/M_Texture ")
                                    print(j+"/M_Texture ")
                            f1.write(tail[-1]+"/E_Texture ")
                            print(tail[-1]+"/E_Texture ")
                            # f1.write(name + '\t' +tail+'\t'+'has_texture'+' '+sentM+'\n')
                            # f4.write(titles[i] +',has_organ,'+name+'\n')
                            # f4.write(name+',has_texture,'+tail+'\n')
                            # f4.write(titles[i]+','+name+'质地,'+tail+'\n')
                        elif '形' in id and '形成' not in id:
                            if partFlag:
                                # xz1 = id.split(part)[1].replace('。','').replace('；','')
                                continue
                            else:
                                xz1 = id.split('、')[0].replace('。','').replace('；','')
                            if '花瓣' in id and '形' in  id.split('花瓣')[1]:
                                f1.write(name + '\t' +id.split('花瓣')[1].split('、')[0].replace('；','').replace('。','')+'\t'+'has_shape'+' '+sentM+'\n')
                                f4.write(titles[i] +',has_organ,'+name+'\n')
                                f4.write(name+',has_shape,'+id.split('花瓣')[1].split('、')[0].replace('；','').replace('。','')+'\n')
                                f4.write(titles[i]+','+name+'形状,'+id.split('花瓣')[1].split('、')[0].replace('；','').replace('。','')+'\n')

                            elif name in id and '形' in  id.split(name)[1]:
                                f1.write(name + '\t' +id.split(name)[1].split('、')[0].replace('；','').replace('。','')+'\t'+'has_shape'+' '+sentM+'\n')
                                f4.write(titles[i] +',has_organ,'+name+'\n')
                                f4.write(name+',has_shape,'+id.split(name)[1].split('、')[0].replace('；','').replace('。','')+'\n')
                                f4.write(titles[i]+','+name+'形状,'+id.split(name)[1].split('、')[0].replace('；','').replace('。','')+'\n')
                            elif '形' in xz1:
                                f1.write(name + '\t' +xz1+'\t'+'has_shape'+' '+sentM+'\n')
                                f4.write(titles[i] +',has_organ,'+name+'\n')
                                f4.write(name+',has_shape,'+xz1+'\n')
                                f4.write(titles[i]+','+name+'形状,'+xz1+'\n')
                        elif '色' in id and '毛' not in id :
                            if partFlag:
                                # se = id.split(part)[1].replace('。','').replace('；','')
                                continue
                            else:
                                se = id.split('、')[0].replace('。','').replace('；','')
                            if '花瓣' in id and '色' in  id.split('花瓣')[1]:
                                f1.write(name + '\t' +id.split('花瓣')[1].replace('；','').replace('。','')+'\t'+'has_color'+' '+sentM+'\n')
                                f4.write(titles[i] +',has_organ,'+name+'\n')
                                f4.write(name+',has_color,'+id.split('花瓣')[1].replace('；','').replace('。','')+'\n')
                                f4.write(titles[i]+','+name+'颜色,'+id.split('花瓣')[1].replace('；','').replace('。','')+'\n')

                            elif name in id and '色' in id.split(name)[1]:
                                f1.write(name + '\t' +id.split(name)[1].replace('；','').replace('。','')+'\t'+'has_color'+' '+sentM+'\n')
                                f4.write(titles[i] +',has_organ,'+name+'\n')
                                f4.write(name+',has_color,'+id.split(name)[1].replace('；','').replace('。','')+'\n')
                                f4.write(titles[i]+','+name+'颜色,'+id.split(name)[1].replace('；','').replace('。','')+'\n')
                            elif '色' in  se:
                                f1.write(name + '\t' +se+'\t'+'has_color'+' '+sentM+'\n')
                                f4.write(titles[i] +',has_organ,'+name+'\n')
                                f4.write(name+',has_color,'+se+'\n')
                                f4.write(titles[i]+','+name+'颜色,'+se+'\n')

                        elif '宽' in id and '米' in id and id.split('宽')[1].replace('；','').replace('。','')!='':
                            f1.write(name + '\t' +id.split('宽')[1].replace('；','').replace('。','')+'\t'+'has_width'+' '+sentM+'\n')
                            f4.write(titles[i] +',has_organ,'+name+'\n')
                            f4.write(name+',has_width,'+id.split('宽')[1].replace('；','').replace('。','')+'\n')
                            f4.write(titles[i]+','+name+'宽,'+id.split('宽')[1].replace('；','').replace('。','')+'\n')

                        elif '高' in id and '米' in id and id.split('高')[1].replace('。','').replace('；','')!='':
                            f1.write(name + '\t' +id.split('高')[1].replace('。','').replace('；','')+'\t'+'has_height'+' '+sentM+'\n')
                            f4.write(titles[i] +',has_organ,'+name+'\n')
                            f4.write(name+',has_height,'+id.split('高')[1].replace('。','').replace('；','')+'\n')
                            f4.write(titles[i]+','+name+'高,'+id.split('高')[1].replace('；','').replace('。','')+'\n')
                        elif flagJ:
                            if '直径' in id and '米' in id and id.split('直径')[1].replace('。','').replace('；','')!='':
                                f1.write(name + '\t' +id.split('直径')[1].replace('。','').replace('；','')+'\t'+'has_diameter'+' '+sentM+'\n')
                                f4.write(titles[i] +',has_organ,'+name+'\n')
                                f4.write(name+',has_diameter,'+id.split('直径')[1].replace('。','').replace('；','')+'\n')
                                f4.write(titles[i]+','+name+'直径,'+id.split('直径')[1].replace('。','').replace('；','')+'\n')
                            else:
                                f1.write(name + '\t' +id.split('径')[1].replace('。','').replace('；','')+'\t'+'has_diameter'+' '+sentM+'\n')
                                f4.write(titles[i] +',has_organ,'+name+'\n')
                                f4.write(name+',has_diameter,'+id.split('径')[1].replace('。','').replace('；','')+'\n')
                                f4.write(titles[i]+','+name+'直径,'+id.split('径')[1].replace('。','').replace('；','')+'\n')
                        elif sent_cut[0] in id:
                            if flagN and id.split('花瓣')[1].replace('；','').replace('。','')!='':
                                f1.write(name + '\t' +id.split('花瓣')[1].replace('；','').replace('。','')+'\t'+'has_quantity'+' '+sentM+'\n')
                                f4.write(titles[i] +',has_organ,'+name+'\n')
                                f4.write(name+',has_quantity,'+id.split('花瓣')[1].replace('；','').replace('。','')+'\n')
                                f4.write(titles[i]+','+name+'数量,'+id.split('花瓣')[1].replace('；','').replace('。','')+'\n')
                    f1.write(name + '\t' +sentO.split('形，长')[1].split('，')[0].split('；')[0].split('。')[0]+'\t'+'has_length'+' '+sentM+'\n')
                    f4.write(titles[i] +',has_organ,'+name+'\n')
                    f4.write(name+',has_length,'+sentO.split('形，长')[1].split('，')[0].split('；')[0].split('。')[0]+'\n')
                    f4.write(titles[i]+','+name+'长,'+sentO.split('形，长')[1].split('，')[0].split('；')[0].split('。')[0]+'\n')


                elif '长、宽' not in sentO:

                    nameN = sent_cut[0]
                    for id in sentO.split('，'):
                        partFlag = False
                        seqName = ''
                        id_cuts = jieba.lcut(id)
                        f = re.findall(r'[^\*"/:?\\|()（）<>]',id)
                        g = "".join(f)
                        flagN =re.search(r'{}\d'.format(nameN),g)
                        flagJ =re.search(r'{}\d'.format('径'),id)
                        name = nameN
                        for id_cut in id_cuts:
                            if '质' in id_cut:
                                tail =id_cut
                            for head in dic:
                                if id_cut == head:
                                    nameN =id_cut
                                    flagN =re.search(r'{}\d'.format(nameN),g)
                            name1 = nameN
                            # name = nameN
                            for be in dicB:
                                if id_cut == be:
                                    nameP = id_cut
                                    # name = nameN + id_cut
                                    part = id_cut
                                    partFlag = True
                            for sequence in dicSeq:
                                if id_cut == sequence:
                                    seqName = id_cut
                        if partFlag == False:
                            name = nameN
                        if seqName != '':
                            f1.write(name + '\t' +seqName+'\t'+'has_growth_form'+' '+sentM+'\n')
                            f4.write(titles[i] +',has_organ,'+name+'\n')
                            f4.write(name+',has_growth_form,'+seqName)
                            f4.write(titles[i]+','+name+'生长型,'+seqName)
                        if '质' in id and tail != '质' and tail != '质地' and tail != '蛋白质':
                            f1.write(name + '\t' +tail+'\t'+'has_texture'+' '+sentM+'\n')
                            f4.write(titles[i] +',has_organ,'+name+'\n')
                            f4.write(name+',has_texture,'+tail)
                            f4.write(titles[i]+','+name+'质地,'+tail)

                        elif '形' in id and '形成' not in id:
                            if partFlag:
                                # xz1 = id.split(part)[1].replace('。','').replace('；','')
                                continue
                            else:
                                xz1 = id.split('、')[0].replace('。','').replace('；','')
                            if '花瓣' in id and '形' in  id.split('花瓣')[1]:
                                f1.write(name + '\t' +id.split('花瓣')[1].split('、')[0].replace('；','').replace('。','')+'\t'+'has_shape'+' '+sentM+'\n')
                                f4.write(titles[i] +',has_organ,'+name+'\n')
                                f4.write(name+',has_shape,'+id.split('花瓣')[1].split('、')[0].replace('；','').replace('。','')+'\n')
                                f4.write(titles[i]+','+name+'形状,'+id.split('花瓣')[1].split('、')[0].replace('；','').replace('。','')+'\n')

                            elif name in id and '形' in  id.split(name)[1]:
                                f1.write(name + '\t' +id.split(name)[1].split('、')[0].replace('；','').replace('。','')+'\t'+'has_shape'+' '+sentM+'\n')
                                f4.write(titles[i] +',has_organ,'+name+'\n')
                                f4.write(name+',has_shape,'+id.split(name)[1].split('、')[0].replace('；','').replace('。','')+'\n')
                                f4.write(titles[i]+','+name+'形状,'+id.split(name)[1].split('、')[0].replace('；','').replace('。','')+'\n')
                            elif '形' in xz1:
                                f1.write(name + '\t' +xz1+'\t'+'has_shape'+' '+sentM+'\n')
                                f4.write(titles[i] +',has_organ,'+name+'\n')
                                f4.write(name+',has_shape,'+xz1+'\n')
                                f4.write(titles[i]+','+name+'形状,'+xz1+'\n')
                        elif '色' in id and '毛' not in id :
                            if partFlag:
                                # se = id.split(part)[1].replace('。','').replace('；','')
                                continue
                            else:
                                se = id.split('、')[0].replace('。','').replace('；','')
                            if '花瓣' in id and '色' in  id.split('花瓣')[1]:
                                f1.write(name + '\t' +id.split('花瓣')[1].replace('；','').replace('。','')+'\t'+'has_color'+' '+sentM+'\n')
                                f4.write(titles[i] +',has_organ,'+name+'\n')
                                f4.write(name+',has_color,'+id.split('花瓣')[1].replace('；','').replace('。','')+'\n')
                                f4.write(titles[i]+','+name+'颜色,'+id.split('花瓣')[1].replace('；','').replace('。','')+'\n')

                            elif name in id and '色' in id.split(name)[1]:
                                f1.write(name + '\t' +id.split(name)[1].replace('；','').replace('。','')+'\t'+'has_color'+' '+sentM+'\n')
                                f4.write(titles[i] +',has_organ,'+name+'\n')
                                f4.write(name+',has_color,'+id.split(name)[1].replace('；','').replace('。','')+'\n')
                                f4.write(titles[i]+','+name+'颜色,'+id.split(name)[1].replace('；','').replace('。','')+'\n')
                            elif '色' in  se:
                                f1.write(name + '\t' +se+'\t'+'has_color'+' '+sentM+'\n')
                                f4.write(titles[i] +',has_organ,'+name+'\n')
                                f4.write(name+',has_color,'+se+'\n')
                                f4.write(titles[i]+','+name+'颜色,'+se+'\n')

                        elif '宽' in id and '米' in id and id.split('宽')[1].replace('；','').replace('。','')!='':
                            f1.write(name + '\t' +id.split('宽')[1].replace('；','').replace('。','')+'\t'+'has_width'+' '+sentM+'\n')
                            f4.write(titles[i] +',has_organ,'+name+'\n')
                            f4.write(name+',has_width,'+id.split('宽')[1].replace('；','').replace('。','')+'\n')
                            f4.write(titles[i]+','+name+'宽,'+id.split('宽')[1].replace('；','').replace('。','')+'\n')

                        elif '高' in id and '米' in id and id.split('高')[1].replace('。','').replace('；','')!='':
                            f1.write(name + '\t' +id.split('高')[1].replace('。','').replace('；','')+'\t'+'has_height'+' '+sentM+'\n')
                            f4.write(titles[i] +',has_organ,'+name+'\n')
                            f4.write(name+',has_height,'+id.split('高')[1].replace('。','').replace('；','')+'\n')
                            f4.write(titles[i]+','+name+'高,'+id.split('高')[1].replace('；','').replace('。','')+'\n')
                        elif flagJ:
                            if '直径' in id and '米' in id and id.split('直径')[1].replace('。','').replace('；','')!='':
                                f1.write(name + '\t' +id.split('直径')[1].replace('。','').replace('；','')+'\t'+'has_diameter'+' '+sentM+'\n')
                                f4.write(titles[i] +',has_organ,'+name+'\n')
                                f4.write(name+',has_diameter,'+id.split('直径')[1].replace('。','').replace('；','')+'\n')
                                f4.write(titles[i]+','+name+'直径,'+id.split('直径')[1].replace('。','').replace('；','')+'\n')
                            else:
                                f1.write(name + '\t' +id.split('径')[1].replace('。','').replace('；','')+'\t'+'has_diameter'+' '+sentM+'\n')
                                f4.write(titles[i] +',has_organ,'+name+'\n')
                                f4.write(name+',has_diameter,'+id.split('径')[1].replace('。','').replace('；','')+'\n')
                                f4.write(titles[i]+','+name+'直径,'+id.split('径')[1].replace('。','').replace('；','')+'\n')
                        elif '长' in id and '米' in id and id.split('长')[1].replace('。','').replace('；','')!='':
                            f1.write(name + '\t' +id.split('长')[1].replace('。','').replace('；','')+'\t'+'has_length'+' '+sentM+'\n')
                            f4.write(titles[i] +',has_organ,'+name+'\n')
                            f4.write(name+',has_length,'+id.split('长')[1].replace('。','').replace('；','')+'\n')
                            f4.write(titles[i]+','+name+'长,'+id.split('长')[1].replace('。','').replace('；','')+'\n')

                        elif flagN and '花瓣' in id and id.split('花瓣')[1].replace('；','').replace('。','')!='':
                            f1.write(name + '\t' +id.split('花瓣')[1].replace('；','').replace('。','')+'\t'+'has_quantity'+' '+sentM+'\n')
                            f4.write(titles[i] +',has_organ,'+name+'\n')
                            f4.write(name+',has_quantity,'+id.split('花瓣')[1].replace('；','').replace('。','')+'\n')
                            f4.write(titles[i]+','+name+'数量,'+id.split('花瓣')[1].replace('；','').replace('。','')+'\n')

            else:
                nameN = sent_cut[0]

                for id in sentO.split('，'):
                    partFlag = False
                    seqName = ''
                    id_cuts = jieba.lcut(id)
                    f = re.findall(r'[^\*"/:?\\|()（）<>]',id)
                    g = "".join(f)
                    flagN =re.search(r'{}\d'.format(nameN),g)
                    flagJ =re.search(r'{}\d'.format('径'),id)

                    name = nameN
                    for id_cut in id_cuts:
                        if '质' in id_cut:
                            tail =id_cut
                        if '状' in id_cut:
                            zhuang = id_cut
                        for head in dic:
                            if id_cut == head:
                                nameN =id_cut
                                flagN =re.search(r'{}\d'.format(nameN),g)
                        # name = nameN
                        for be in dicB:
                            if id_cut == be:
                                nameP = id_cut
                                # name = nameN + id_cut
                                part = id_cut
                                partFlag = True
                        for sequence in dicSeq:
                            if id_cut == sequence:
                                seqName = id_cut
                    if partFlag == False:
                        name = nameN
                    if seqName != '':
                        if name == '叶':
                            f1.write(name + '\t' +seqName+'\t'+'has_growth_form'+' '+sentM+'\n')
                            f4.write(titles[i] +',has_organ,'+name+'\n')
                            f4.write(name+',has_growth_form,'+seqName)
                            f4.write(titles[i]+','+name+'生长型,'+seqName)
                        else:
                            f3.write(name + '\t' +seqName+'\t'+'r '+sentM+'\n')
                            # f4.write(titles[i] +','+name+'生长型,'+seqName+'\n')
                            # print(titles[i] + '\t' +seqName+'\t'+name+' '+sentM+'\n')
                            f5.write(seqName+'\n')
                    elif '质' in id and tail != '质' and tail != '质地' and tail != '蛋白质' and tail != '质叶痕' and tail !='':
                        if name == '叶':
                            f1.write(name + '\t' +tail+'\t'+'has_texture'+' '+sentM+'\n')
                            f4.write(titles[i] +',has_organ,'+name+'\n')
                            f4.write(name+',has_texture,'+tail)
                            f4.write(titles[i]+','+name+'质地,'+tail)

                        else:
                            f3.write(name + '\t' +tail+'\t'+'r '+sentM+'\n')
                            # f4.write(name +',花瓣质地,'+tail+'\n')
                            # print(titles[i] + '\t' +tail+'\t'+name+' '+sentM+'\n')
                            f5.write(tail+'\n')
                    elif '形' in id and '形成' not in id:
                        if partFlag:
                            # xz1 = id.split(part)[1].replace('。','').replace('；','')
                            continue
                        else:
                            xz1 = id.split('、')[0].replace('。','').replace('；','')
                        print(sentM+'  '+id)
                        if name in id:
                            xz = id.split(name)[1].split('、')[0].replace('。','').replace('；','')
                            if '形' in xz:
                                if '：' in xz:
                                    f3.write(name + '\t' +xz.split('：')[1] +'\t'+'r '+sentM+'\n')
                                else:
                                    f3.write(name + '\t' +xz +'\t'+'r '+sentM+'\n')
                        elif '形' in xz1:
                            if '：' in xz1:
                                f3.write(name + '\t' +xz1.split('：')[1]+'\t'+'r '+sentM+'\n')
                            else:
                                f3.write(name + '\t' +xz1+'\t'+'r '+sentM+'\n')
                    elif '状' in id and '羽状' not in id:
                        if partFlag:
                            # xz1 = id.split(part)[1].replace('。','').replace('；','')
                            continue
                        else:
                            xz1 = id.split('、')[0].replace('。','').replace('；','')
                        print(sentM+'  '+id)
                        if name in id:
                            xz = id.split(name)[1].split('、')[0].replace('。','').replace('；','')
                            if '状' in xz:
                                if '：' in xz:
                                    f3.write(name + '\t' +xz.split('：')[1] +'\t'+'r '+sentM+'\n')
                                else:
                                    f3.write(name + '\t' +xz +'\t'+'r '+sentM+'\n')
                        elif '状' in xz1:
                            if '：' in xz1:
                                f3.write(name + '\t' +xz1.split('：')[1]+'\t'+'r '+sentM+'\n')
                            else:
                                f3.write(name + '\t' +xz1+'\t'+'r '+sentM+'\n')
                    elif '色' in id and '毛' not in id:
                        if name in id :
                            se = id.split(name)[1].replace('。','').replace('；','')
                            if '色' in se:
                                f3.write(name + '\t' +se+'\t'+'r '+sentM+'\n')
                        elif partFlag:
                            se = id.split(part)[1].replace('。','').replace('；','')
                            if '色' in se:
                                f3.write(name + '\t' +se+'\t'+'r '+sentM+'\n')
                        else:
                            se = id.replace('。','').replace('；','')
                            if '色' in se:
                                f3.write(name + '\t' +se+'\t'+'r '+sentM+'\n')
                    elif '宽' in id and '米' in id and id.split('宽')[1].replace('。','').replace('；','')!='':
                        f3.write(name + '\t' +id.split('宽')[1].replace('。','').replace('；','')+'\t'+'r '+sentM+'\n')
                    elif '长' in id and '米' in id and id.split('长')[1].replace('。','').replace('；','')!='':
                        f3.write(name + '\t' +id.split('长')[1].replace('。','').replace('；','')+'\t'+'r '+sentM+'\n')
                    elif '高' in id and '米' in id and id.split('高')[1].replace('。','').replace('；','')!='':
                        if name == '茎':
                            f1.write(name + '\t' +id.split('高')[1].replace('。','').replace('；','')+'\t'+'has_height'+' '+sentM+'\n')
                            f4.write(titles[i] +',has_organ,'+name+'\n')
                            f4.write(name+',has_height,'+id.split('高')[1].replace('。','').replace('；','')+'\n')
                            f4.write(titles[i]+','+name+'高,'+id.split('高')[1].replace('；','').replace('。','')+'\n')
                        else:
                            f3.write(name + '\t' +id.split('高')[1].replace('。','').replace('；','')+'\t'+'r '+sentM+'\n')
                        # f4.write(titles[i] +','+name+'高,'+id.split('高')[1].replace('；','').replace('。','')+'\n')
                    elif flagJ:
                        if '直径' in id and '米' in id and id.split('直径')[1].replace('。','').replace('；','')!='':
                            if name == '蒴果':
                                f1.write(name + '\t' +id.split('直径')[1].replace('。','').replace('；','')+'\t'+'has_diameter'+' '+sentM+'\n')
                                f4.write(titles[i] +',has_organ,'+name+'\n')
                                f4.write(name+',has_diameter,'+id.split('直径')[1].replace('。','').replace('；','')+'\n')
                                f4.write(titles[i]+','+name+'直径,'+id.split('直径')[1].replace('。','').replace('；','')+'\n')
                            else:
                                f3.write(name + '\t' +id.split('直径')[1].replace('。','').replace('；','')+'\t'+'r '+sentM+'\n')
                        else:
                            if name == '蒴果':
                                f1.write(name + '\t' +id.split('径')[1].replace('。','').replace('；','')+'\t'+'has_diameter'+' '+sentM+'\n')
                                f4.write(titles[i] +',has_organ,'+name+'\n')
                                f4.write(name+',has_diameter,'+id.split('径')[1].replace('。','').replace('；','')+'\n')
                                f4.write(titles[i]+','+name+'直径,'+id.split('径')[1].replace('。','').replace('；','')+'\n')
                            else:
                                f3.write(name + '\t' +id.split('径')[1].replace('。','').replace('；','')+'\t'+'r '+sentM+'\n')
                        # f4.write(titles[i] +','+name+'直径,'+id.split('直径')[1].replace('；','').replace('。','')+'\n')
                    elif name in id:
                        if flagN and id.split(name)[1].replace('；','').replace('。','')!='':
                            f3.write(name + '\t' +id.split(name)[1].replace('；','').replace('。','')+'\t'+'r '+sentM+'\n')



def main():
    input_path = 'E:\学习\毕业论文文献及项目\项目\KnowledgeGraph_Agriculture-master\Plants\plantTxt\\train\\plant_train.csv'
    # input_path = 'E:\学习\毕业论文文献及项目\项目\KnowledgeGraph_Agriculture-master\Plants\plantTxt\\train\\test_train.csv'
    # input_path = 'E:\学习\毕业论文文献及项目\项目\KnowledgeGraph_Agriculture-master\Plants\plantTxt\\otherTriple.csv'
    # input_path = 'E:\学习\毕业论文文献及项目\项目\KnowledgeGraph_Agriculture-master\Plants\\plant_norm.csv'
    output_path = 'E:\学习\毕业论文文献及项目\项目\KnowledgeGraph_Agriculture-master\Plants\\nerOutput.txt'
    myltp(input_path=input_path, output_path=output_path)

if __name__ == '__main__':
    main()
