import os, glob
import nltk

nltk.download('punkt')
from nltk.tokenize import word_tokenize

def remove_stopwords(artifact, title):
    raw_content = ""
    with open(os.path.join("full-articles", artifact, title)) as read_f:
        raw_content = word_tokenize(read_f.read())
        stopword_free = [word for word in raw_content if word not in stopwords]
        with open("stopword-free/" + artifact + "/" + title, "w+") as write_f:
            write_f.write((' '.join(stopword_free)))

if __name__ == "__main__":
    stopwords = []

    # Read in Stopword file
    with open("VoyantEnglishStopWords.txt", "r") as f:
        stopwords = f.read().splitlines()
        f.close()

    artifacts = ['google', 'tiktok', 'chatgpt']

    for artifact in artifacts:
        directory = os.path.join("full-articles", artifact)
        for article in os.listdir(directory):
            remove_stopwords(artifact, article)


