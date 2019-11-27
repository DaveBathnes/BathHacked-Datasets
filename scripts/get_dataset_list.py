import csv
import json
import requests
import unicodedata
import re

DATA_OUTPUT = '../data/datasets.csv'

def run():

    datasets = []

    catalogue = requests.get('https://data.bathhacked.org/data.json').json()

    # Complete the dataset list
    for dataset in catalogue['dataset']:
        datasets.append(
            [
                dataset['title'],
                dataset['modified'],
                dataset['description'],
            ]
        )

    with open(DATA_OUTPUT, 'w', encoding='utf8', newline='') as out_csv:
        writer = csv.writer(out_csv, delimiter=',',
                                quotechar='"', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(
            ['title', 'description', 'updated'])
        for dataset in datasets:
            writer.writerow([dataset[0], dataset[1], dataset[2]])

    # Download all the datasets
    for dataset in catalogue['dataset']:
        for distribution in dataset['distribution']:
            if distribution['mediaType'] == 'text/csv':
                download_url = distribution['downloadURL']
                download_file(download_url, get_valid_filename(dataset['title'] + '.csv'))

def download_file(url, filename):
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open('../data/' + filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192): 
                if chunk:
                    f.write(chunk)
    return filename

def get_valid_filename(s):
    s = str(s).strip().replace(' ', '_')
    return re.sub(r'(?u)[^-\w.]', '', s)

run()
