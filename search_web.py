# search_web.py

import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, parse_qs, unquote

from config import HEADERS, MAX_RESULTS, REQUEST_TIMEOUT
from utils import normalize, extract_main_text

# Fallback to Bing HTML search for reliable scraping
BING_SEARCH_URL = "https://www.bing.com/search"


def clean_ddg_url(url: str) -> str:
    """
    Clean DuckDuckGo proxy URLs of the form
    "//duckduckgo.com/l/?uddg=<encoded_url>"
    by extracting and decoding the uddg parameter.
    """
    if url.startswith("//duckduckgo.com/l/"):
        parsed = urlparse(url, scheme="https")
        qs = parse_qs(parsed.query)
        uddg = qs.get('uddg')
        if uddg:
            return unquote(uddg[0])
    return url


def search_web(query: str):
    """
    Perform a web search for `query` using Bing's HTML interface,
    returning a list of (url, snippet) tuples.
    Also handles cleaning DuckDuckGo proxy URLs if encountered.
    """
    try:
        resp = requests.get(
            BING_SEARCH_URL,
            params={"q": query},
            headers=HEADERS,
            timeout=REQUEST_TIMEOUT
        )
        resp.raise_for_status()
    except requests.RequestException as e:
        print(f"[ERROR] Failed to fetch Bing search results: {e}")
        return []

    soup = BeautifulSoup(resp.text, "html.parser")
    results = []

    # Each result lives in an <li class="b_algo">
    for item in soup.find_all('li', class_='b_algo', limit=MAX_RESULTS):
        h2 = item.find('h2')
        a = h2.find('a') if h2 else None
        if not a or not a.get('href'):
            continue
        url = a['href']

        # Clean any DuckDuckGo proxy URL
        url = clean_ddg_url(url)

        # Extract snippet text
        snippet_tag = item.find('p')
        snippet_text = snippet_tag.get_text(' ', strip=True) if snippet_tag else ''

        # Fallback: fetch page and extract text if no snippet
        if not snippet_text:
            try:
                page_resp = requests.get(url, headers=HEADERS, timeout=REQUEST_TIMEOUT)
                page_resp.raise_for_status()
                full = extract_main_text(page_resp.text)
                snippet_text = " ".join(normalize(full).split()[:50]) + "…"
            except Exception:
                snippet_text = ''

        results.append((url, snippet_text))

    if not results:
        print("[DEBUG] No results found. Check CSS selectors or network connectivity.")
    return results
