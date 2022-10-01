import json
from dataset_handler import build_popular_books_corpus, build_specific_corpus
from postprocessing import *

with open("config.json") as f:
    config = json.load(f)

config_build_corpus = config["corpus"]["build"]
config_corpus_name = config["corpus"]["name"]
config_word_cloud = config["postprocessing"]["word_cloud"]
config_count_vectorizer = config["postprocessing"]["count_vectorizer"]
config_tfidf = config["postprocessing"]["tfidf"]
config_word2vec = config["postprocessing"]["word2vec"]
base_path = config["corpus"]["path"]
config_text_start = config["corpus"]["text_start"]
config_text_end = config["corpus"]["text_end"]
config_paging = config["corpus"]["paging"]

if config_build_corpus:
    if config_corpus_name == 'popular':
        build_popular_books_corpus(text_start=config_text_start, text_end=config_text_end)
    else:
        build_specific_corpus(config_corpus_name, paging=config_paging, text_start=config_text_start, text_end=config_text_end)

filenames = listdir(base_path)
data = []
if config_word_cloud:
    print(f"Word cloud from corpus: {base_path}")
    text = ''
    for filename in filenames:
        f = open(base_path + filename)
        text += f.read()

    generate_word_cloud(text)
    generate_word_cloud(text, ignore=True)

if config_count_vectorizer or config_tfidf:

    filenames = listdir(base_path)
    data = []
    for filename in filenames:
        f = open(base_path + filename)
        data.append(f.read())

    if config_count_vectorizer:
        print(f"Count Vectorizer from corpus: {base_path}")
        count_vectorizer(data)
    if config_tfidf:
        print(f"TF-IDF: {base_path}")
        vocabulary = tfidf(data)

if config_word2vec:
    print(f"Word2vec example from ../corpus/105.txt")
    f = open("../corpus/105.txt", "r")
    word2vec(text=f.read(), key='lady')




