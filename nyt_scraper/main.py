
import requests
from requests_html import HTMLSession
import os
from article import Article

NYT_API_KEY = ""
BASE_REQUEST_STRING = "https://api.nytimes.com/svc/search/v2/articlesearch.json?q=chatgpt&api-key=fbtqV1nw5AXMJngJG3BxcEnnJtdYNsCd" #'https://api.nytimes.com/svc/search/v2/articlesearch.json'

SEARCH_TERM = "chatgpt"
ARTICLES_PATH = "nyt_scraper/articles_current"
INVALID_CHARS = [",", "’", "‘", "?", "!", "%", "|", ":", "<", ">"]
REPLACE_CHAR = {"’": "'"}
PAGE_SIZE = 200
ARTICLE_LIMIT = 200
DATES = [
    ["2022-09-01", "2022-12-31"],
    ["2023-01-01", "2023-04-18"],
]

def clean_title(title):
    new_title = ""
    for i, c in enumerate(title):
        if c == "’" and (i > 0 and title[i - 1] != " ") and \
            (i < len(title) - 1 and title[i + 1] != " " and 
            title[i + 1] not in INVALID_CHARS):
            new_title += "'"
            continue
        if c in INVALID_CHARS:
            continue
        new_title += c
    return new_title

def get_articles(page_number, limit):
    #query = f"?q={SEARCH_TERM}&api-key={NYT_API_KEY}"#&show-fields=bodyText"\
            #f"&page={page_number}&page-size={PAGE_SIZE}"
            #f"&page={page_number}&from-date={start_date}&to-date={end_date}&"\
            #f"page-size={PAGE_SIZE}"
    request_string = BASE_REQUEST_STRING #+ query
    response = requests.get(request_string)
    results = response.json()["response"]["docs"]
    articles = []
    for result in results:
        title = result["headline"]['main']
        date = result["pub_date"]
        try:
            web_url = (result['web_url'])
        except IndexError:
            web_url = None
        
        if (web_url != None):
            ##Retrieve the page using https get method
            page = requests.get(web_url)

            session = HTMLSession()
            page = session.get(web_url)

            paragraphs = page.html.find("p.css-at9mc1")
            body = ""
            for i in range(len(paragraphs)):
                body = body + paragraphs[i].text + " "
                
            if body != "":
                article = Article(title, date, body)
                articles.append(article)
                if (len(articles) >= limit):
                    break

    if not os.path.exists(ARTICLES_PATH):
        os.mkdir(ARTICLES_PATH)
    for article in articles:
        with open(f"{ARTICLES_PATH}/{article.title}_{article.date}", "w") as file:
            file.write(article.body)
    return len(articles)

def main():
    num_articles = 0
    page_number = 0
    while (num_articles < ARTICLE_LIMIT):
        page_number += 1
        num_articles += get_articles(page_number, ARTICLE_LIMIT - num_articles)


if __name__ == "__main__":
    main()