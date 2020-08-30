
# 处理BILSTM+ATT-CRF网络识别出的药用植物防治的疾病实体，得到（植物名称,功用，治疾病）三元组

if __name__ == "__main__":
    disease_dic = []
    with open('E:\学习\毕业论文文献及项目\项目\KnowledgeGraph_Agriculture-master\Plants\disease_dic.txt',encoding='UTF-8-sig') as fin:
        for line in fin.readlines():
            disease_dic.append(line.split(' ')[0])
    fout = open('E:\\学习\\深度学习相关\\ChineseNER_plant\\tensorflow\\funcTriple.csv', encoding='utf8', mode='w')
    fout1 = open('E:\\学习\\深度学习相关\\ChineseNER_plant\\tensorflow\\funcTriple_testify.csv', encoding='utf8', mode='w')
    fout.write("entity,relation,value"+'\n')
    with open('E:\\学习\\深度学习相关\\ChineseNER_plant\\tensorflow\\func_extract.txt', encoding = 'utf8') as fin:
        for line in fin:
            line = line.replace('\n','')
            if 'Disease:' in line:
                plantName = line.split(',')[0]
                for i,id in zip(range(len(line.split('Disease:'))),line.split('Disease:')):
                    if i == 0:
                        continue
                    else:
                        diseaseV = ''
                        value = id.replace(' ','')
                        if id.replace(' ','')[0] == '疗':
                            value = id.replace(' ','').replace('疗','')
                        for disease in disease_dic:
                            if value == disease:
                                diseaseV =value
                        if '《' in value or '》' in value:
                            continue
                        elif diseaseV != '':
                            print(plantName+',治疗,'+diseaseV)
                            fout.write(plantName+',治疗,'+diseaseV+'\n')
                        else:
                            fout1.write(plantName+',治疗,'+value+'\n')
