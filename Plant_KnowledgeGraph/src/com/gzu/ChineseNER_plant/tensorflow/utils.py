# coding=utf-8
import codecs
import re

import jieba
import numpy as np
from twisted.python.compat import raw_input
import matplotlib.pyplot as plt

def calculate(x,y,id2word,id2tag,res=[]):
    entity=[]
    for i in range(len(x)): #for every sen
        for j in range(len(x[0])): #for every word
            if x[i][j]==0 or y[i][j]==0:
                continue

            if id2tag[y[i][j]][0]=='B':
                entity=[id2word[x[i][j]]+'/'+id2tag[y[i][j]]]
            elif id2tag[y[i][j]][0]=='M' and len(entity)!=0 and entity[-1].split('/')[1][1:]==id2tag[y[i][j]][1:]:
                entity.append(id2word[x[i][j]]+'/'+id2tag[y[i][j]])
            elif id2tag[y[i][j]][0]=='E' and len(entity)!=0 and entity[-1].split('/')[1][1:]==id2tag[y[i][j]][1:]:
                entity.append(id2word[x[i][j]]+'/'+id2tag[y[i][j]])
                entity.append(str(i))
                entity.append(str(j))
                res.append(entity)
                entity=[]
            else:
                entity=[]
    return res
    
def get_entity(x,y,id2tag):
    entity=""
    res=[]
    for i in range(len(x)): #for every sen
        for j in range(len(x[i])): #for every word
            if y[i][j]==0:
                continue
            # if id2tag[y[i][j]][0]=='S':
            #     entity=id2tag[y[i][j]][2:]+':'+x[i][j]
            #     res.append(entity)
            #     entity=[]
            if id2tag[y[i][j]][0]=='B':
                entity=id2tag[y[i][j]][2:]+':'+x[i][j]
            elif id2tag[y[i][j]][0]=='M' and len(entity)!=0 :
                entity+=x[i][j]
            elif id2tag[y[i][j]][0]=='E' and len(entity)!=0 :
                entity+=x[i][j]
                res.append(entity)
                entity=[]
            else:
                entity=[]
    return res    
    
def write_entity(outp,x,y,id2tag):
    '''
    注意，这个函数每次使用是在文档的最后添加新信息。
    '''
    entity=''
    for i in range(len(x)): 
        if y[i]==0:
            continue
        # if id2tag[y[i]][0]=='S':
        #     entity=id2tag[y[i]][2:]+':'+x[i]
        #     outp.write(entity+' ')
        #     entity=''
        if id2tag[y[i]][0]=='B':
            entity=id2tag[y[i]][2:]+':'+x[i] 
        elif id2tag[y[i]][0]=='M' and len(entity)!=0:
            entity+=x[i]
        elif id2tag[y[i]][0]=='E'  and len(entity)!=0:
            entity+=x[i] 
            outp.write(entity+' ')
            entity=''
        else:
            entity=''       
    return



accuracys_tr = []
recalls_tr=[]
f_tr = []
accuracys_te = []
recalls_te=[]
f_te = []
def train(model,sess,saver,epochs,batch_size,data_train,data_test,id2word,id2tag):    
    batch_num = int(data_train.y.shape[0] / batch_size)  
    batch_num_test = int(data_test.y.shape[0] / batch_size) 
    for epoch in range(epochs):
        for batch in range(batch_num): 
            x_batch, y_batch = data_train.next_batch(batch_size)
            # print(x_batch.shape
            feed_dict = {model.input_data:x_batch, model.labels:y_batch}
            pre,_ = sess.run([model.viterbi_sequence,model.train_op], feed_dict)
            acc = 0
            if batch%200==0:
                for i in range(len(y_batch)):
                    for j in range(len(y_batch[0])):
                        if y_batch[i][j]==pre[i][j]:
                            acc+=1
                # print(float(acc)/(len(y_batch)*len(y_batch[0])))
        path_name = "./model/model"+str(epoch)+".ckpt"
        # print(path_name)
        if epoch%1==0:
            saver.save(sess, path_name)
            # print("model has been saved")
            entityres=[]
            entityall=[]
            for batch in range(batch_num): 
                x_batch, y_batch = data_train.next_batch(batch_size)
                feed_dict = {model.input_data:x_batch, model.labels:y_batch}
                pre = sess.run([model.viterbi_sequence], feed_dict)
                pre = pre[0]
                entityres = calculate(x_batch,pre,id2word,id2tag,entityres)
                entityall = calculate(x_batch,y_batch,id2word,id2tag,entityall)
            jiaoji = [i for i in entityres if i in entityall]
            if len(jiaoji)!=0:
                accuracy = float(len(jiaoji))/len(entityres)
                recall = float(len(jiaoji))/len(entityall)
                f = float(2*accuracy*recall)/(accuracy+recall)
                accuracys_tr.append(accuracy)
                recalls_tr.append(recall)
                f_tr.append(f)
                print("-------------------------------------train-------------------------------------")
                # print("accuracy:", accuracy)
                # print("recall:", recall)
                # print("f:", f)
                # print("accuracy_tr:", accuracys_tr)
                # print("recall_tr:", recalls_tr)
                # print("f_tr:", f_tr)
                print('Epoch: {}/{} train accuracy: {:.4f}, train recall: {:.4f}, train f: {:.4f}'
                      .format(epoch+1, epochs, accuracy, recall, f))
            else:
                print("accuracy:",0)

            entityres=[]
            entityall=[]
            for batch in range(batch_num_test): 
                x_batch, y_batch = data_test.next_batch(batch_size)
                feed_dict = {model.input_data:x_batch, model.labels:y_batch}
                pre = sess.run([model.viterbi_sequence], feed_dict)
                pre = pre[0]
                entityres = calculate(x_batch,pre,id2word,id2tag,entityres)
                entityall = calculate(x_batch,y_batch,id2word,id2tag,entityall)
            jiaoji = [i for i in entityres if i in entityall]
            if len(jiaoji)!=0:
                accuracy = float(len(jiaoji))/len(entityres)
                recall = float(len(jiaoji))/len(entityall)
                f = float(2*accuracy*recall)/(accuracy+recall)
                accuracys_te.append(accuracy)
                recalls_te.append(recall)
                f_te.append(f)
                print("-------------------------------------test-------------------------------------")
                # print("accuracy:", accuracy)
                # print("recall:", recall)
                # print("f:", f)
                # print("accuracy_te:", accuracys_te)
                # print("recall_te:", recalls_te)
                # print("f_te:", f_te)
                print('Epoch: {}/{} test accuracy: {:.4f}, test recall: {:.4f}, test f: {:.4f}'
                      .format(epoch+1, epochs, accuracy, recall, f))
            else:
                print("accuracy:",0)


    plt.title('train')
    plt.plot(np.arange(len(accuracys_tr)), accuracys_tr, label = 'train accuracy')
    plt.plot(np.arange(len(recalls_tr)), recalls_tr, label = 'train  recall')
    plt.plot(np.arange(len(f_tr)), f_tr, label = 'train  f')
    plt.legend()
    plt.show()
    plt.title('test')
    plt.plot(np.arange(len(accuracys_te)), accuracys_te, label = 'test accuracy')
    plt.plot(np.arange(len(recalls_te)), recalls_te, label = 'test  recall')
    plt.plot(np.arange(len(f_te)), f_te, label = 'test  f')
    plt.legend()
    plt.show()


max_len = 100
def padding(ids):
    if len(ids) >= max_len:  
        return ids[:max_len]
    else:
        ids.extend([0]*(max_len-len(ids)))
        return ids      
def padding_word(sen):
    if len(sen) >= max_len:
        return sen[:max_len]
    else:
        return sen           
                  
def test_input(model,sess,word2id,id2tag,batch_size):
    while True:
        print('-'*60)
        te = ''
        text = raw_input("Enter sentence input: ")
        text = re.split(u'[,，。！？、‘’“”（）；]', text)
        # for id in text:
        #     te += id
        # text = jieba.lcut(te)
        text_id=[]
        for sen in text:
            word_id=[]
            for word in sen:
                if word in word2id:
                    word_id.append(word2id[word])
                else:
                    word_id.append(word2id["unknow"])
            text_id.append(padding(word_id))
        zero_padding=[]
        zero_padding.extend([0]*max_len)
        text_id.extend([zero_padding]*(batch_size-len(text_id)))    
        feed_dict = {model.input_data:text_id}
        pre = sess.run([model.viterbi_sequence], feed_dict)
        entity = get_entity(text,pre[0],id2tag)
        print('result:')
        for i in entity:
            print(i)
        print('-'*60)
            

            
def extraction(input_path,output_path,model,sess,word2id,id2tag,batch_size):
    text_id=[]
    text = []
    text1 = []
    with codecs.open(input_path,'r',encoding='utf-8') as inp:
        for line in inp.readlines():
            plantName = line.split('，')[0]
            line= '治'+line.split('治')[1]
            line = re.split('[：，。！？、‘’“”（）；]', line.strip())

            for sentence in line:
                if sentence=='' or sentence==' ':
                    continue
                word_id=[]
                for word in sentence:
                    if word in word2id:
                        word_id.append(word2id[word])
                    else:
                        word_id.append(word2id["unknow"])
                text_id.append(padding(word_id))
                text.append(padding_word(sentence))
                text1.append(padding_word(plantName+','+sentence))
    zero_padding=[]
    zero_padding.extend([0]*max_len)
    text_id.extend([zero_padding]*(batch_size-len(text_id)%batch_size)) 
    text_id = np.asarray(text_id)
    text_id = text_id.reshape(-1,batch_size,max_len)
    predict = []
    for index in range(len(text_id)):
        feed_dict = {model.input_data:text_id[index]}
        pre = sess.run([model.viterbi_sequence], feed_dict)
        predict.append(pre[0])
    predict = np.asarray(predict).reshape(-1,max_len)
    
    with codecs.open(output_path,'w',encoding='utf-8') as outp:
        for index in range(len(text)):
            print(text1[index]+"   ")
            outp.write(text1[index]+"   ")
            write_entity(outp,text[index],predict[index],id2tag)
            outp.write('\n')
        


