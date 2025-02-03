import pprint
from collections import Counter

from api.web.scan import get_web_page_summary
from utils import get_deduped_sources, get_sources

file_path = "gdelt_data/20250107100000.export.CSV"

def urlSources(file_path):
  sources = get_sources(file_path)
  cSources = Counter(sources)
  filteredSources = {url : count for url, count in cSources.items() if count > 2}
  sortedSources = sorted(filteredSources.items(), key=lambda item: item[1], reverse=True)
  return [{"url": url, "count": count} for url, count in sortedSources]


if __name__ == "__main__":
  sources = get_sources(file_path)
  deduped = get_deduped_sources(file_path)
  cSources = Counter(sources)
  filteredSources = {url : count for url, count in cSources.items() if count > 2}
  sortedSources = sorted(filteredSources.items(), key=lambda item: item[1], reverse=True)
  # pprint.pprint(sortedSources)
  obj = get_web_page_summary(sortedSources[7][0])
  print(obj)
  
  
  