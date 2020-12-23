# Import the hashlib library :
import hashlib as hl


# Show available hash functions :
def show_hash_algorithms():
    tab = sorted(list(filter(lambda v: "_" not in v, hl.algorithms_guaranteed)))
    print(tab)


# Algorithms :
def blake2b(word):
    return hl.blake2b(word.encode('UTF-8')).hexdigest()


def blake2s(word):
    return hl.blake2s(word.encode('UTF-8')).hexdigest()


def md5(word):
    return hl.md5(word.encode('UTF-8')).hexdigest()


def sha1(word):
    return hl.sha1(word.encode('UTF-8')).hexdigest()


def sha224(word):
    return hl.sha224(word.encode('UTF-8')).hexdigest()


def sha256(word):
    return hl.sha256(word.encode('UTF-8')).hexdigest()


def sha384(word):
    return hl.sha384(word.encode('UTF-8')).hexdigest()


def sha512(word):
    return hl.sha512(word.encode('UTF-8')).hexdigest()