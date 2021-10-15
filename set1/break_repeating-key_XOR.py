import requests
from base64 import b64decode
from itertools import combinations
from collections import defaultdict
import math
import string


# Taken from https://opendata.stackexchange.com/questions/7042/ascii-character-frequency-analysis
character_frequencies = defaultdict(int)

# sample text to calculate frequiencies
print("Downloading sample text for calculating character frequencies")
url = "http://ocw.mit.edu/ans7870/6/6.006/s08/lecturenotes/files/t8.shakespeare.txt"
text = requests.get(url).text

for c in text:
    if c in string.printable:
        character_frequencies[c] += (1 / len(text))

def main():
    file_text = requests.get("https://cryptopals.com/static/challenge-data/6.txt").text

    cipher = b64decode(file_text)

    # guessed length of the key ~2 to 40
    key_size = determine_key_size(2, 40, cipher)

    key = bytearray()

    for key_index in range(0, key_size):
        # make blocks of byte_index bytes and solve
        byte_block = bytes(b for byte_index, b in enumerate(cipher) if byte_index % key_size == key_index)
        byte_block_key = findLikelyBasedOnCharFreq(byte_block)[0]
        key.append(byte_block_key)

    print(f"Key: {key}")
    print()

    # now apply the found key to the ciphertext
    plaintext = repeatedXOR(cipher, key)
    print(plaintext.decode())


def findLikelyBasedOnCharFreq(buf: bytes) -> tuple:
    key_and_score = []
    for pkey in range(128):
        result = bytes(pkey ^ input_byte for input_byte in buf)
        score = sum((result.count(key.encode()) + result.count(key.upper().encode())) * value for key, value in character_frequencies.items())
        key_and_score.append((pkey, score))
    key_and_score.sort(key=lambda d: d[1], reverse=True)
    return key_and_score[0]

def key_gen(key: bytes) -> bytes:
    i = 0
    while True:
        yield key[i]
        i += 1
        i %= len(key)
     
def repeatedXOR(message: bytes, key: bytes) -> bytes:
    buffer_xor = bytes(message_byte ^ key_byte for message_byte, key_byte in zip(message, key_gen(key)))
    return buffer_xor

def hamming_distance(buf_a: bytes, buf_b: bytes):
    return sum(bin(a ^ b).count('1') for a,b in zip(buf_a, buf_b))

def test_hamming_distance():
    assert hamming_distance(b"this is a test", b"wokka wokka!!!") == 37

def determine_key_size(min_key_size: int, max_key_size: int, cipher: bytes):
    lowest_diff = float("inf")
    key_size = 0
    for possible_key_size in range(min_key_size, max_key_size+1):
        grouping = [cipher[i:i+possible_key_size] for i in range(0, len(cipher), possible_key_size)]
        diff_score = sum(hamming_distance(a, b) / possible_key_size for a,b in combinations(grouping, 2))  / math.comb(len(grouping), 2)
        if diff_score < lowest_diff:
            key_size = possible_key_size
            lowest_diff = diff_score
    return key_size

main()
