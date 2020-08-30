import logging
from gensim.models import word2vec

def main():
    logging.basicConfig(format="%(asctime)s:%(levelname)s:%(message)s",level=logging.INFO)
    # sentences = word2vec.LineSentence("plant_segwords.txt")
    sentences = word2vec.LineSentence("iplant_segwords.txt")
    # size：单词向量的维度。
    model = word2vec.Word2Vec(sentences,size=100)
    # model = word2vec.Word2Vec(sentences,size=15)
    #保存模型
    #model.save("../model/wiki_corpus.bin")
    # model.save("wiki_corpus_100.txt")
    model.wv.save_word2vec_format("vector_15.txt")

if __name__ == "__main__":
    main()
