# BARD - NLP Story Generator

BARD is a Story Generator using Transformers (Work in Progress). 
It obtains certain books from Gutenberg API, such as popular books or specific corpus. (Ex. Vampire books)

## How to use

### Requirements
- Python 3.8

### Installation
1. Clone repository with SSH:
```bash
$> git clone git@github.com:eugepineiro/nlp-txt-generator.git
```
2. Install required modules from requirements.txt:
```bash
$> pip3 install -r scripts/requirements.txt
```
### Configuration & Execution
Customize `config.json`:

| Parameter          | Description                                                                  | Options |
|--------------------|------------------------------------------------------------------------------|---------|
| "corpus"           | Configuration params to build corpus                                         |         |
| "build"            | Generate corpus                                                              | boolean |
| "name"             | Corpus name. "popular" or specific topic. Ex: "vampire"                      | string  |
| "path"             | Path where corpus has been saved                                             | string  |
| "text_start"       | Save text from text_start                                             | int     |
| "text_end"         | Save text until text_end. If text_end = -1 saves whole book from text_start  | int     |
| "paging"           | Page to start scraping from in specific corpus                               | int     |
| "postprocessing"   | Configuration params to build corpus                                         |         |
| "word_cloud"       | Plot wordcloud                                                               | boolean |
| "count_vectorizer" | Run Count Vectorizer algorithm                                               | boolean |
| "tfidf"            | Run TFIDF algorithm                                                          | boolean |
| "word2vec"         | Run Word2Vec algorithm                                                       | boolean |

Exec program with:
```bash
$> python3 main.py
```

### Example configurations: `config.json`
```json
{
  "corpus": {
    "build": true,
    "name": "popular",
    "path": "../corpus/",
    "text_start": 0,
    "text_end": -1,
    "paging": 1
  },
  "postprocessing": {
    "word_cloud": true,
    "count_vectorizer": false,
    "tfidf": false,
    "word2vec": true
  }
}
```

```json
{
  "corpus": {
    "build": true,
    "name": "vampire",
    "path": "../vampire_corpus/", 
    "text_start": 20,
    "text_end": -1,
    "paging": 1
  },
  "postprocessing": {
    "word_cloud": true,
    "count_vectorizer": false,
    "tfidf": false,
    "word2vec": false
  }
}
```
