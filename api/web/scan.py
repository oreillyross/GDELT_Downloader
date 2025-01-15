import requests
from bs4 import BeautifulSoup


def get_web_page_summary(url):
  try:
    response = requests.get(url, timeout=10)
    response.raise_for_status()
  except requests.exceptions.RequestException as e:
    return f"An error occured fetching the webpage {e}"

  try:
    soup = BeautifulSoup(response.text, "html.parser")
    title = soup.title.string if soup.title else "No Title found"
    paragraph = soup.find('p')
    summary = paragraph.get_text(
        strip=True) if paragraph else "No summary found"
    return {"title": title, "summary": summary, "url": url}
  except Exception as e:
    return f"Unable to parse the webpage {e}"
