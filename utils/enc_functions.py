import codecs
import base64

<<<<<<< Updated upstream
def get_standard_text_encodings():
=======
ASCII_BINARY_ENCODINGS=[
    'base64',
    'base32',
    'base16',
    'Ascii85',
    'base85'
]

ASCII_BINARY_FUNCTION=[
    {'base64': 'b64'},
    {'base32': 'b32'},
    {'base16': 'b16'},
    {'Ascii85': 'a85'},
    {'base85': 'b85'}
]

"""def get_standard_text_encodings():
>>>>>>> Stashed changes
    version, url = ('3.9', 'https://docs.python.org/3.9/library/codecs.html#standard-encodings')
    html = requests.get(url).text
    doc = lxml.html.fromstring(html)
    standard_encodings_table = doc.xpath('//*[@id="standard-encodings"]/table')[0]
    encodings = standard_encodings_table.xpath('.//td[1]/p/text()')
    return encodings
"""

def encode(message, encoding):
    function = ASCII_BINARY_FUNCTION['encoding'] + 'encode'
    return base64.function(message).decode('utf-8')


def decode(message, encoding):
    function = ASCII_BINARY_FUNCTION['encoding'] + 'decode'
    return base64.function(message).decode('utf-8')

def encode_text(encoding, text):
    """ convert unicoded strings into any encodings supported by the current version of Python """

    #encoded_text = text.encode(encoding, 'strict')
    encoded_text = codecs.encode(text, encoding)
    return base64.b64encode(encoded_text).decode('utf-8')

def decode_text(encoding, text):
    """ convert encoded strings (with any encodings supported by the current version of Python) to unicoded string """

    #decoded_text = bytes(text, encoding='utf-8').decode(encoding, errors="ignore")

<<<<<<< Updated upstream
    #decoded_text = codecs.decode(base64_decode(text), encoding)
    return base64.b64decode(text)
=======
    # decoded_text = codecs.decode(base64_decode(text), encoding)
    return base64.b64decode(text).decode('utf-8')
>>>>>>> Stashed changes
