# utils.py
import string
from readability import Document  # optional

# simple punctuation stripper
PUNCT_TRANS = str.maketrans(string.punctuation, " " * len(string.punctuation))

def normalize(text: str) -> str:
    return text.lower().translate(PUNCT_TRANS).strip()

def extract_main_text(html: str) -> str:
    """
    If you installed readability-lxml, you can:
      doc = Document(html)
      return doc.summary()
    Otherwise, fallback to extracting all <p> tags.
    """
    from bs4 import BeautifulSoup
    soup = BeautifulSoup(html, "html.parser")
    for tag in soup(["script", "style", "nav", "footer", "header"]):
        tag.decompose()
    return " ".join(p.get_text(" ", strip=True) for p in soup.find_all("p"))
