import re
import string


def extract_links(text):
    match = re.search('(?P<url>https?://[^\s]+)', text).group('url')
    result = [match] if match else []
    while match:
        text = re.sub(match, '', text)
        mo = re.search('(?P<url>https?://[^\s]+)', text)
        match = mo.group('url') if mo else None
        if match:
            result.append(match)
    return result


def normalize(text):
    text = text.translate(text.maketrans({c: '' for c in string.punctuation}))
    text = re.sub(' +', ' ', text)
    return text.lower()
