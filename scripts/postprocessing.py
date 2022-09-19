from wordcloud import WordCloud
import matplotlib.pyplot as plt
import re, string
from os import listdir
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from gensim.models import Word2Vec

def generate_word_cloud(text, ignore=False):
    if ignore:
        print("ignoring words")

        text = text.lower()

        shortword = re.compile(r'\W*\b\w{1,3}\b') # Ignore short words
        text = shortword.sub('', text)

        generic_vocabulary = ['chapter', 'will', 'made','come','great','good','much', 'upon', 'thee', 'thou']
        for word in generic_vocabulary:
            text = text.replace(word, '')

    wordcloud = WordCloud().generate(text)

    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")
    plt.show()

def count_vectorizer(train_data):
    cv = CountVectorizer(
        ngram_range=[1, 1], # just using unigrams
        max_df=0.8, min_df=2,
        max_features=None,
        stop_words="english" # delete stopwords
    )
    matrix = cv.fit_transform(train_data)
    vocabulary = cv.get_feature_names_out()
    print(matrix)   # (número de documento, índice de la palabra en cv.get_feature_names_out()) cantidad de apariciones
    print(f'Vocabulario: {vocabulary}')
    print(f'Tamaño: {len(vocabulary)}')

def tfidf(train_data):
    # Tmb relaciona los docs ademas de darme la freq
    tfidf = TfidfVectorizer(ngram_range=[1, 1], max_df=0.8, min_df=2, max_features=None, stop_words="english")
    matrix = tfidf.fit_transform(train_data)
    vocabulary = tfidf.get_feature_names_out()
    print(matrix)  # (número de documento, índice de la palabra en cv.get_feature_names_out()) frecuencia de la palabra
    print(f'Vocabulario: {vocabulary}')
    print(f'Tamaño: {len(vocabulary)}')

    return vocabulary

def word2vec(text):

    lines = text.replace('\n', ' ')
    lines = lines.split(' ')

    # make all characters lower
    lines = [line.lower() for line in lines]

    # remove punctuations from each line
    lines = [line.translate(str.maketrans('', '', string.punctuation)) for line in lines]

    # tokenize
    # lines = word_tokenize(lines)



    model = Word2Vec(
        sentences=[lines],
        min_count=1,
        sg=1,
        window=7
    )

    print(model.wv.most_similar('hola'))

word2vec('hola como estas esto es un gaucho')