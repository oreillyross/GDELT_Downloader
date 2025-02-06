import csv
import os

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


def get_deduped_sources(file_path):
  sources = get_sources(file_path)
  return set(sources)

def get_latest_file(directory):
  files = [
      f for f in os.listdir(directory)
      if os.path.isfile(os.path.join(directory, f))
  ]

  if not files:
    return None

  latest_file = max(files,
                    key=lambda f: os.path.getmtime(os.path.join(directory, f)))

  return os.path.join(directory, latest_file)
