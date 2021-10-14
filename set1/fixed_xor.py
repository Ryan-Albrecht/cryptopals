def fixed_xor(buffer_a: bytes, buffer_b: bytes) -> bytes:
    assert len(buffer_a) == len(buffer_b)
    buffer_xor = bytes(a ^ b for (a, b) in zip(buffer_a, buffer_b))
    return buffer_xor

def main():
    buffer_a = bytes.fromhex(input("Buffer A (in hex): "))
    buffer_b = bytes.fromhex(input("Buffer B (in hex): "))
    result = fixed_xor(buffer_a, buffer_b)
    print(result.hex())

def test_solution():
    buffer_a = bytes.fromhex("1c0111001f010100061a024b53535009181c")
    buffer_b = bytes.fromhex("686974207468652062756c6c277320657965")
    result = fixed_xor(buffer_a, buffer_b)
    assert result.hex() == "746865206b696420646f6e277420706c6179"