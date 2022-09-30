from wordcloud import WordCloud
import matplotlib.pyplot as plt
import re, string, nltk
import pandas as pd
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
    :return: vocabulary
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
    print(f'Vocabulary: {vocabulary}')
    print(f'Size: {len(vocabulary)}')

    return vocabulary

def tfidf(train_data):
    """
    TFIDF. Prints vocabulary matrix

    :param train_data: string array (documents) to train
    :return: vocabulary
    """

    tfidf = TfidfVectorizer(
        ngram_range=[1, 1],                   # Just using unigrams (words)
        max_df=0.8,                           # When building the vocabulary ignore terms that have a document frequency strictly higher than the given threshold
        min_df=0.1,                           # When building the vocabulary ignore terms that have a document frequency strictly lower than the given threshold
        max_features=None,                    # Consider all features
        analyzer='word',                      # To remove stopwords
        stop_words=stopwords.words('english') # List that contains stop words, all of which will be removed from the resulting tokens. Only applies if analyzer == 'word'. There are several known issues when ‘english’ string is used so this is the alternative
    )
    matrix = tfidf.fit_transform(train_data)
    vocabulary = tfidf.get_feature_names_out()
    print(f"TFIDF Matrix (number of document, word index) frequency \n{matrix}")

    df = pd.DataFrame(matrix[0].T.todense(), index=tfidf.get_feature_names_out(), columns=["TF-IDF"])
    df = df.sort_values('TF-IDF', ascending=False)

    top_n_words = 25
    print(f"\nTop {top_n_words} frequent words\n {df.head(25)}")

    """
    Another way to see most_frequent_words
    most_frequent_words = matrix.argmax(axis=1)
    print(most_frequent_words[0][0])

    for i in range(len(most_frequent_words)):
        index = most_frequent_words[i].min()
        print(f"Word: {vocabulary[index]} Freq: {matrix[(0,index)]}")
    """
    print(f'\nWhole vocabulary: {vocabulary}')
    print(f'\nVocabulary size: {len(vocabulary)}')

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
