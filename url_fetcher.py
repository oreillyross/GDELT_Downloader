import argparse
from collections import defaultdict
import csv
from bs4 import BeautifulSoup

import requests

from constants import gdelt_columns


def get_sources(file_path):

  event_data = []
  with open(file_path, 'r', encoding='utf-8') as file:
    reader = csv.reader(file, delimiter='\t')
    for row in reader:
      event_data.append(dict(zip(gdelt_columns, row)))
    sources = []
    for event in event_data:
      sources.append(event['SOURCEURL'])
    return sources


mentions = {}


def isMentioned(source, keyword):
  try:
    headers = {
        'User-Agent':
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.81 Safari/537.36'
    }
    response = requests.get(source, headers=headers)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'html.parser')
    return keyword.lower() in soup.get_text().lower()
  except requests.exceptions.RequestException as e:
    print(f"Error fetching the url, {e}")
    return False


def search(sources, keyword):
  mentions = {}
  for source in sources:
    print(f"fetching: {source}")
    mentioned = isMentioned(source, keyword)
    if mentioned:
      mentions[source] = keyword
  return mentions


if __name__ == "__main__":
  parser = argparse.ArgumentParser(
      description="Read GDELT Data and save to SQLite")

  parser.add_argument("filename", help="Path to the GDELT file")

  args = parser.parse_args()

  sources = get_sources(args.filename)
  mentions = search(sources[:10], "kamala")
  print(mentions)
