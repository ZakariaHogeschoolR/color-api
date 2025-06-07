import string

import string

def build_vocab():
    allowed_chars = list("#0123456789ABCDEF[], \"") + list(string.ascii_uppercase) + [' ', '.', '?', '!', ':']
    # Add START and END tokens if needed:
    allowed_chars += ['<START>', '<END>']  # optional, if you use tokens
    vocab = sorted(set("".join(allowed_chars)))  # flatten tokens if needed
    char2idx = {ch: idx for idx, ch in enumerate(vocab)}
    idx2char = {idx: ch for ch, idx in char2idx.items()}
    return vocab, char2idx, idx2char


def preprocess_line(line, allowed_chars):
    # Convert to uppercase
    line = line.strip().upper()
    # Remove any char not in allowed chars
    filtered_line = "".join([c for c in line if c in allowed_chars])
    # Add start and end tokens if you want:
    filtered_line = "<START>" + filtered_line + "<END>"
    return filtered_line


def decode(indices, idx2char):
    return "".join([idx2char[i] for i in indices])
