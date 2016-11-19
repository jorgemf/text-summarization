# coding=utf-8
import json
import logging
from time import sleep

import requests
from bs4 import BeautifulSoup

SUBREDDIT_URL = 'http://www.reddit.com/r/worldnews/new.json'
USER_AGENT = 'text sum scrapper 1.0'


def parse_text(description):
    # Add space around symbols and split sentences
    description = description.replace('...', '.')
    description = description.replace('.', ' . </s> <s> ')
    description = description.replace(',', ' , ')
    description = description.replace('\'', ' \' ')
    description = description.replace('\"', ' \" ')
    description = description.replace(';', ' ; ')
    description = description.replace('?', ' ? </s> <s> ')
    description = description.replace('!', ' ! </s> <s> ')
    description = description.replace(':', ' : ')
    description = description.replace('\t', ' ')
    description = description.replace('\n', ' ')
    description = description.replace('\r', ' ')
    description = description.replace('  ', ' ')
    description = description.replace('  ', ' ')
    return description


def process_html_page(page_url):
    logging.info('GET {}'.format(page_url))
    r = requests.get(page_url, headers={'User-agent': USER_AGENT})
    soup = BeautifulSoup(r.content, 'html.parser')
    head = soup.find('head')
    title = head.find('meta', property='og:title')
    if title:
        title = title['content']
    description = head.find('meta', property='og:description')
    if description:
        description = description['content']
    return title, description


def get_examples_from_json(page_json):
    for example in page_json['data']['children']:
        if 'url' in example['data']:
            yield example['data']['url']


def process_reddit_page(page_url):
    logging.info('GET {}'.format(page_url))
    r = requests.get(page_url, headers={'User-agent': USER_AGENT})
    while r.status_code == 429:
        logging.info('too many requests, sleeping 30')
        sleep(30)
        logging.info('GET {}'.format(page_url))
        r = requests.get(page_url)
    return json.loads(r.content)


def add_vocabulary(d, sentence):
    # words = re.sub('[^\w]', ' ', sentence).split()
    words = sentence.split(' ')
    for word in words:
        word = word.strip()
        if len(word) > 0:
            if word in d:
                d[word] += 1
            else:
                d[word] = 1


def download_examples(output_file, examples):
    vocabulary = {}
    with open(output_file, 'w') as file:
        size = 0
        next_url = SUBREDDIT_URL
        while size < examples:
            page_json = process_reddit_page(next_url)
            next_url = '{}?after='.format(SUBREDDIT_URL, page_json['data']['after'])
            for example_url in get_examples_from_json(page_json):
                title, description = process_html_page(example_url)
                if title is not None and description is not None:
                    description = parse_text(description)
                    title = parse_text(title)
                    title = u'<d> <p> <s> {} </s> </p> </d>'.format(title).encode('ascii', 'ignore')
                    description = u'<d> <p> <s> {} </s> </p> </d>'.format(description).encode('ascii', 'ignore')
                    file.write(u'article= {} \t abstract= {} \t publisher=reddit? \n'.format(description, title))
                    add_vocabulary(vocabulary, title)
                    add_vocabulary(vocabulary, description)
                    size += 1
    return vocabulary

def order(key, value):
    if key.startswith('<'):
        return -value
    return value

def save_vocabulary(vocabulary):
    sorted_voc = sorted(vocabulary.items(), key=lambda x: order(x[0],x[1]), reverse=True)
    with open('vocabulary.txt', 'w') as file:
        for word, items in sorted_voc:
            file.write('{} {}\n'.format(word, items))
        file.write('<PAD> 1\n')
        file.write('<UNK> 1\n')


if __name__ == '__main__':
    FORMAT = '%(asctime)-15s %(message)s'
    logging.basicConfig(level=logging.DEBUG, format=FORMAT)
    import argparse

    parser = argparse.ArgumentParser(prog='Download a dataset form reddit')
    parser.add_argument('--examples', metavar='examples', type=int,
                        help='Number of examples to download')
    args = parser.parse_args()

    vocabulary = download_examples('examples_reddit.txt', args.examples)
    save_vocabulary(vocabulary)
