import sys
from glob import glob

INVALID_CHARS = set([',', '‘', '?', '!', '%', '|', ':', '<', '>', '“', '”',
                    '•'])
APOSTROPHES = set(['’', '’'])

def clean_article(article_text):
    text_to_process = article_text.split('•')[0].strip()
    new_article_text = ''
    for i, c in enumerate(text_to_process):
        if c in APOSTROPHES and (i > 0 and text_to_process[i - 1] != ' ') and \
            (i < len(text_to_process) - 1 and text_to_process[i + 1] != ' ' and 
            text_to_process[i + 1] not in INVALID_CHARS):
            new_article_text += "'"
            continue
        elif c == '–' and (i > 0 and text_to_process[i - 1] == ' ') and \
            (i < len(text_to_process) - 1 and text_to_process[i + 1] == ' '):
            # Remove trailing space
            new_article_text = new_article_text[:-1]
            continue
        elif c in INVALID_CHARS:
            continue
        new_article_text += c
    return new_article_text


def main():
    if len(sys.argv) != 2:
        print('Usage: python clean_articles.py <articles folder path>')
        return
    
    articles_path = sys.argv[1]
    article_names = glob(articles_path + '/*')
    for article_name in article_names:
        with open(article_name, 'r+') as file:
            content = file.read()
            file.seek(0)
            file.truncate(0)
            file.write(clean_article(content))


if __name__ == '__main__':
    main()