from utils import get_sources, get_deduped_sources 
from collections import Counter
import pprint

file_path = "gdelt_data/20241002134500.export.CSV"

if __name__ == "__main__":
  sources = get_sources(file_path)
  deduped = get_deduped_sources(file_path)
  cSources = Counter(sources)
  filteredSources = {url : count for url, count in cSources.items() if count > 2}
  sortedSources = sorted(filteredSources.items(), key=lambda item: item[1], reverse=True)
  pprint.pprint(sortedSources)
  
  
  