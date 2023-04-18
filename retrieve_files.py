import os, glob
import re
import json
import requests
from os import makedirs, getcwd
from os.path import join, exists
from datetime import date, timedelta


# EXAMPLE URL: ttp://content.guardianapis.com/search?q=tiktok&order-by=newest&show-fields=all&page-size=10&query-fields=webTitle&api-key=1d2e8b51-ecd1-4cc8-91f4-2edc298d5403

API_KEY = '1d2e8b51-ecd1-4cc8-91f4-2edc298d5403'
API_ENDPOINT = 'http://content.guardianapis.com/search'
HTML_TAG_REGEX = re.compile('<.*?>')
GOOGLE_FIELDS = "google AND (algorithm OR search OR ai OR (artificial AND intelligence))"

my_params = {
    # 'tag':"technology",
    'q': GOOGLE_FIELDS,
    'query-fields': "headline",
    'lang': "en",
    'from-date': "2000-01-01",
    'to-date': "2015-03-1",
    'order-by': "newest",
    'show-fields': 'all',
    'page':5,
    'page-size': 50,
    'api-key': API_KEY
}


def generate_filename(id):
    '''
    Input: The "id" field of a Guardian article, i.e., the URL portion unique to the article
    Output: a string filename in yyyy_mmm_dd_article-title
    '''
    # Replace slashes with underscores
    filename = id.replace("/", "_")
    find_date = re.search(r'\d{4}', filename)
    # Truncate tags from id
    filename = filename[find_date.start():]

    return filename


def iterate_day():
    '''
    TODO delete
    Disused reference methodby Dan Nguyen
    '''
    # day iteration from here:
    # http://stackoverflow.com/questions/7274267/print-all-day-dates-between-two-dates

    # Sample URL
#
# http://content.guardianapis.com/search?from-date=2016-01-02&
# to-date=2016-01-02&order-by=newest&show-fields=all&page-size=200
# &api-key=your-api-key-goes-here
    start_date = date(2023, 3, 1)
    end_date = date(2023, 3, 1)
    dayrange = range((end_date - start_date).days + 1)
    for daycount in dayrange:
        dt = start_date + timedelta(days=daycount)
        datestr = dt.strftime('%Y-%m-%d')
        fname = join(ARTICLES_DIR, datestr + '.json')
        if not exists(fname):
            # then let's download it
            print("Downloading", datestr)
            all_results = []
            my_params['from-date'] = datestr
            my_params['to-date'] = datestr
            current_page = 1
            total_pages = 1
            while current_page <= total_pages:
                print("...page", current_page)
                my_params['page'] = current_page
                resp = requests.get(API_ENDPOINT, my_params)
                data = resp.json()
                all_results.extend(data['response']['results'])
                # if there is more than one page
                current_page += 1
                total_pages = data['response']['pages']

            with open(fname, 'w') as f:
                print("Writing to", fname)

                # re-serialize it for pretty indentation
                f.write(json.dumps(all_results, indent=2))


if __name__ == "__main__":

    print(os.getcwd())

    # Perform request
    response_data = requests.get(API_ENDPOINT, my_params).json()
    articles = response_data["response"]["results"]

    # Generate files
    for article in articles:
        # Remove HTML tags from article body
        body = article["fields"]["body"]
        body = re.sub(HTML_TAG_REGEX, '', body)
        # Create filename
        filename = generate_filename(article["id"])

        with open("google/" + filename, 'w+') as f:
            f.write(body)
            f.close()
