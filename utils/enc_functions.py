import requests
import lxml.html
import codecs


def get_standard_text_encodings():
    version, url = ('3.9', 'https://docs.python.org/3.9/library/codecs.html#standard-encodings')
    html = requests.get(url).text
    doc = lxml.html.fromstring(html)
    standard_encodings_table = doc.xpath('//*[@id="standard-encodings"]/table')[0]
    encodings = standard_encodings_table.xpath('.//td[1]/p/text()')
    return encodings


def encode_text(encoding, text):
    """ convert unicoded strings into any encodings supported by the current version of Python """

    encoded_text = text.encode(encoding, 'strict')

    return encoded_text


def decode_text(encoding, text):
    """ convert encoded strings (with any encodings supported by the current version of Python) to unicoded string """

    decoded_text = bytes(text, encoding='utf-8').decode(encoding, errors="ignore")

    return decoded_text


def encode_file(encoding, file):
    return


def decode_file(encoding, file):
    return
