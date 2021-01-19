import codecs
import base64

from src.logic.encoding.constants import ASCII_BINARY_FUNCTION

"""def get_standard_text_encodings():

    version, url = ('3.9', 'https://docs.python.org/3.9/library/codecs.html#standard-encodings')
    html = requests.get(url).text
    doc = lxml.html.fromstring(html)
    standard_encodings_table = doc.xpath('//*[@id="standard-encodings"]/table')[0]
    encodings = standard_encodings_table.xpath('.//td[1]/p/text()')
    return encodings
"""

def encode(message, encoding):
    function = ASCII_BINARY_FUNCTION[encoding] + 'encode'
    return getattr(base64, function)(bytes(message, encoding='utf-8')).decode('utf-8')


def decode(message, encoding):
    function = ASCII_BINARY_FUNCTION[encoding] + 'decode'
    return getattr(base64, function)(message).decode('utf-8')


def encode_text(encoding, text):
    """ convert unicoded strings into any encodings supported by the current version of Python """

    # encoded_text = text.encode(encoding, 'strict')
    encoded_text = codecs.encode(text, encoding)
    return base64.b64encode(encoded_text).decode('utf-8')

def decode_text(encoding, text):
    """ convert encoded strings (with any encodings supported by the current version of Python) to unicoded string """

    # decoded_text = bytes(text, encoding='utf-8').decode(encoding, errors="ignore")

    # decoded_text = codecs.decode(base64_decode(text), encoding)
    return base64.b64decode(text)

    # decoded_text = codecs.decode(base64_decode(text), encoding)
    return base64.b64decode(text).decode('utf-8')

