SYM_ALGORITHMS = [
    'AES',
    'TripleDES',
    'CAST5',
    'SEED',
    'Camellia',
    'Blowfish',
    'IDEA',
]


def key_sizes_gen(min_size, max_size):
    key_sizes = []
    x = min_size
    while x <= max_size:
        key_sizes.append(x)
        x = x + 8
    return key_sizes


SYM_ALGORITHMS_PROPS = {
    'AES': {'security': 1, 'key_sizes': [128, 192, 256], 'block_size': 128},
    'TripleDES': {'security': 1, 'key_sizes': [64, 128, 192], 'block_size': 64},
    'CAST5': {'security': 1, 'key_sizes': key_sizes_gen(40, 148), 'block_size': 64},
    'SEED': {'security': 1, 'key_sizes': [128], 'block_size': 128},
    'Camellia': {'security': 1, 'key_sizes': [128, 192, 256], 'block_size': 128},
    'Blowfish': {'security': 0, 'key_sizes': key_sizes_gen(32, 448), 'block_size': 64},
    'IDEA': {'security': 0, 'key_sizes': [128], 'block_size': 64}
}
