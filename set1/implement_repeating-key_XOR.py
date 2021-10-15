def key_gen(key: bytes) -> bytes:
    i = 0
    while True:
        yield key[i]
        i += 1
        i %= len(key)
     
def repeatedXOR(message: bytes, key: bytes) -> bytes:
    buffer_xor = bytes(message_byte ^ key_byte for message_byte, key_byte in zip(message, key_gen(key)))
    return buffer_xor

def main():
    message = input("Text: ").encode()
    key = b"ICE"
    output = repeatedXOR(message, key).hex()
    print(output)

def test_solution():
    text = b"Burning 'em, if you ain't quick and nimble\nI go crazy when I hear a cymbal"
    answer = "0b3637272a2b2e63622c2e69692a23693a2a3c6324202d623d63343c2a26226324272765272a282b2f20430a652e2c652a3124333a653e2b2027630c692b20283165286326302e27282f"
    key = b"ICE"
    assert repeatedXOR(text, key).hex() == answer