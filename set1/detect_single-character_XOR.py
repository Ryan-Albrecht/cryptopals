import string
from collections import defaultdict
import requests

# Taken from https://opendata.stackexchange.com/questions/7042/ascii-character-frequency-analysis
character_frequencies = defaultdict(int)

# sample text to calculate frequiencies
print("Downloading sample text for calculating character frequencies")
url = "http://ocw.mit.edu/ans7870/6/6.006/s08/lecturenotes/files/t8.shakespeare.txt"
text = requests.get(url).text

for c in text:
    if c in string.printable:
        character_frequencies[c] += (1 / len(text))

def findLikelyBasedOnCharFreq(buf: bytes) -> tuple:
    key_and_score = []
    for pkey in range(128):
        result = bytes(pkey ^ input_byte for input_byte in buf)
        score = sum((result.count(key.encode()) + result.count(key.upper().encode())) * value for key, value in character_frequencies.items())
        key_and_score.append((pkey, score))
    key_and_score.sort(key=lambda d: d[1], reverse=True)
    return key_and_score[0]

def main():
    challenge_url = "https://cryptopals.com/static/challenge-data/4.txt"
    results = []
    inputs = requests.get(challenge_url).text.splitlines()
    for index, line in enumerate(inputs):
        key_and_score = findLikelyBasedOnCharFreq(bytes.fromhex(line))
        results.append((*key_and_score, index))
    results.sort(key=lambda d: d[1], reverse=True)
    pkey, score, index = results[0]
    result = bytes(pkey ^ input_byte for input_byte in bytes.fromhex(inputs[index]))
    print(score, " ", result)

main()
