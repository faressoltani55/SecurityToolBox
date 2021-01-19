import hashlib as hl

# Show available hash functions :
def hash_algorithms():
    return sorted(list(filter(lambda v: "_" not in v, hl.algorithms_guaranteed)))


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


def calc_hash(choice, word):
    if choice == "blake2b":
        return blake2b(word)
    elif choice == "blake2s":
        return blake2s(word)
    elif choice == "md5":
        return md5(word)
    elif choice == "sha1":
        return sha1(word)
    elif choice == "sha224":
        return sha224(word)
    elif choice == "sha256":
        return sha256(word)
    elif choice == "sha384":
        return sha384(word)
    elif choice == "sha512":
        return sha512(word)

