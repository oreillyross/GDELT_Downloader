import pprint
from collections import Counter

from utils import get_deduped_sources, get_sources

file_path = "gdelt_data/20241210091500.export.CSV"

def urlSources(file_path):
  sources = get_sources(file_path)
  cSources = Counter(sources)
  filteredSources = {url : count for url, count in cSources.items() if count > 2}
  sortedSources = sorted(filteredSources.items(), key=lambda item: item[1], reverse=True)
  return sortedSources


if __name__ == "__main__":
  sources = get_sources(file_path)
  deduped = get_deduped_sources(file_path)
  cSources = Counter(sources)
  filteredSources = {url : count for url, count in cSources.items() if count > 2}
  sortedSources = sorted(filteredSources.items(), key=lambda item: item[1], reverse=True)
  pprint.pprint(sortedSources)
  
  
  