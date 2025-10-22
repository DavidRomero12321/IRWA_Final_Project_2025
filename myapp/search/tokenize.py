import re, unicodedata
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords

try:
    stopwords.words("english")
except LookupError:
    import nltk; nltk.download("stopwords")

_STEM = PorterStemmer()
_STOP = set(stopwords.words("english"))
_PUNCT = re.compile(r"[^\w\s]+", re.UNICODE)

def build_terms(text: str) -> list[str]:
    if not isinstance(text, str): return []
    s = unicodedata.normalize("NFKC", text.lower())
    s = _PUNCT.sub(" ", s)
    toks = [t for t in s.split() if t not in _STOP]
    toks = [_STEM.stem(t) for t in toks]
    return [t for t in toks if len(t) > 1 and not t.isdigit()]
