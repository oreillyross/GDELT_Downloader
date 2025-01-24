import requests
from bs4 import BeautifulSoup, Comment


def visible_filter(element):
  if element.parent.name in [
      'script', 'meta', 'style', 'head', 'title', 'meta', '[document]'
  ]:
    return False
  
  return not isinstance(element, Comment) 


def get_web_page_summary(url, word_limit=100):
  try:
    response = requests.get(url, timeout=10)
    response.raise_for_status()
  except requests.exceptions.RequestException as e:
    return f"An error occured fetching the webpage {e}"

  try:
    soup = BeautifulSoup(response.text, "html.parser")
    title = soup.title.string if soup.title else "No Title found"
    text_all = soup.find_all(text=True)
    visible_text = filter(visible_filter, text_all)
    full_text = ''.join(chunk.strip() for chunk in visible_text)
    words = full_text.split()
    summary = ' '.join(words[:word_limit])
    return {"title": title, "summary": summary, "url": url}
  except Exception as e:
    return f"Unable to parse the webpage {e}"
