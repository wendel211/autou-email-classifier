import re

STOPWORDS_PT = {
    'a','o','os','as','de','do','da','dos','das','e','é','um','uma','para','por','com',
    'na','no','nas','nos','em','ao','à','às','aos','se','que','sobre','como','mais','menos',
    'já','não','sim','foi','ser','tem','têm','ter','há','ou','até','seu','sua','seus','suas'
}

def normalize(text: str) -> str:
    text = text or ""
    text = text.lower()
    # remove emails/urls números longos e pontuação redundante
    text = re.sub(r'https?://\S+|www\.\S+', ' ', text)
    text = re.sub(r'[\w.-]+@[\w-]+\.[\w.-]+', ' ', text)
    text = re.sub(r'\d{5,}', ' ', text)
    text = re.sub(r'[^a-zà-ú0-9\s]', ' ', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def tokenize(text: str):
    return [t for t in normalize(text).split() if t not in STOPWORDS_PT]
