from base64 import b64encode

def hex_to_base64(hex_str):
    base64 = b64encode(bytes.fromhex(hex_str))
    return base64.decode()

def main():
    hex_str = input("Hex: ")
    base64 = hex_to_base64(hex_str)
    print(base64)

def test_solution():
    hex = "49276d206b696c6c696e6720796f757220627261696e206c696b65206120706f69736f6e6f7573206d757368726f6f6d"
    base64 = "SSdtIGtpbGxpbmcgeW91ciBicmFpbiBsaWtlIGEgcG9pc29ub3VzIG11c2hyb29t"
    assert hex_to_base64(hex) == base64