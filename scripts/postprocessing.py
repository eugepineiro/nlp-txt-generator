from wordcloud import WordCloud
import matplotlib.pyplot as plt
import re, string, nltk
from os import listdir
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from gensim.models import Word2Vec
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

def generate_word_cloud(text, ignore=False):
    """
    Plots word cloud

    :param text: string from where the wordcloud is generated
    :param ignore: remove shortwords, genirc words and stopwords
    :return: void
    """
    if ignore:
        print(text)
        print("ignoring words")

        text = text.lower()

        shortword = re.compile(r'\W*\b\w{1,3}\b') # Ignore short words
        text = shortword.sub('', text)

        generic_vocabulary =['chapter', 'illustration','language','preface',"\'s", 'vatsyayana','one','without','another','anything','admiral','kennedy','something', 'concerning', 'thought', 'tabaqui','edition', 'contain', 'nothing']
        ignore_arr = generic_vocabulary #+ stopwords.words('english')
        for word in ignore_arr:
            text = text.replace(word, '')

    wordcloud = WordCloud().generate(text)

    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")
    plt.show()

def count_vectorizer(train_data):
    """
    Count vectorizer

    :param train_data: words to train
    :return: void, prints vocabulary and sparse matrix
    """
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
    """
    TFIDF. Prints sparse matrix

    :param train_data: words to train
    :return: vocabulury
    """

    tfidf = TfidfVectorizer(ngram_range=[1, 1], max_df=0.8, min_df=2, max_features=None, stop_words="english")
    matrix = tfidf.fit_transform(train_data)
    vocabulary = tfidf.get_feature_names_out()
    print(matrix)  # (número de documento, índice de la palabra en cv.get_feature_names_out()) frecuencia de la palabra

    most_frequent_words = matrix.argmax(axis=1)
    for i in range(len(most_frequent_words)):
        index = most_frequent_words[i][0]
        print(f"Word: {vocabulary[index]} Freq: {matrix[(0,index)]}")

    print(f'Vocabulario: {vocabulary}')
    print(f'Tamaño: {len(vocabulary)}')

    return vocabulary

def word2vec(text, key, clean=True):
    """
    Word2Vec embeddings

    :param text: text to generate embeddings
    :param key: most similar to key
    :param clean: remove punctuations and stopwords
    :return: tokens
    """

    tokens = word_tokenize(text)

    tokens = [token.lower() for token in tokens] # to lowercase

    if clean:
        for token in tokens:
            if token in string.punctuation or token in stopwords.words('english'):
                tokens.remove(token)

    model = Word2Vec(
        sentences=[tokens],
        min_count=1,
        sg=1,
        window=7
    )
    print(model.wv.most_similar(key))

    return tokens
