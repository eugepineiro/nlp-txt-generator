from wordcloud import WordCloud
import matplotlib.pyplot as plt
import re
from os import listdir

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

base_path = '../corpus/'
filenames = listdir(base_path)
text = ''
for filename in filenames:
    f = open(base_path + filename)
    text += f.read()
generate_word_cloud(text)
generate_word_cloud(text, ignore=True)