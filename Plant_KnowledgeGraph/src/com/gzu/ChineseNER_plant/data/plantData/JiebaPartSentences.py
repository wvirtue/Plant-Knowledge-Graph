# 经典的jieba分词，用来将句子打碎 分成一个个中文词
import jieba
import jieba.analyse
import jieba.posseg as pseg
import codecs, sys


def cut_words(sentence):
    # 将词打印
    return " ".join(jieba.cut(sentence)).encode('utf-8')


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("usage:python3 txt txt")
        exit(1)
    target = codecs.open(sys.argv[2], encoding='utf8', mode='w')
    with codecs.open(sys.argv[1], encoding='utf8') as f:
        # f = codecs.open('wiki_01_simp.txt, 'r', encoding="utf8')
        # target = codecs.open("wiki_01_simp_seq.txt", 'w', encoding="utf8")
        print('open files')
        line_num = 1
        line = f.readline()
        line = line.replace('\r','').replace('\n','')
        jieba.load_userdict("E:\\学习\\深度学习相关\\ChineseNER_plant\\tensorflow\\iplant_dic.txt")
        # jieba.load_userdict("E:\\学习\\深度学习相关\\ChineseNER_plant\\tensorflow\\iplant_entityMark.txt")
        while line:
            print('---- processing ', line_num, ' article----------------')
            line_seg = "  ".join(['{0}/{1}'.format(w,t) for w,t in pseg.cut(line)])
            print(line_seg)
            target.writelines(line_seg+'\n')
            line_num = line_num + 1
            line = f.readline()
            line = line.replace('\r','').replace('\n','')
        f.close()
        target.close()
        exit()
        while line:
            curr = []
            for oneline in line:
                # print(oneline)
                curr.append(oneline)
            after_cut = map(cut_words, curr)
            target.writelines(after_cut)
            print('saved', line_num, 'articles')
            exit()
            line = f.readline()
        f.close()
        target.close()

