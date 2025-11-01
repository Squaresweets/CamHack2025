def to_base224(n):
    if n == 0:
        return [0]
    b = []
    while n > 0:
        b.append(n % 224)
        n //= 224
    return b[::-1]

def from_base224(digits):
    n = 0
    for x in digits:
        n = n * 224 + x
    return n

char_to_val = {**{chr(97+i): i for i in range(26)}, ' ':27, ',':28, '.':29, '?':30, '!':31}
val_to_char = {i: chr(97+i) for i in range(26)} | {27:' ', 28:',', 29:'.', 30:'?', 31:'!'}

def to_values(s):
   return [char_to_val[c.lower()] for c in s] + [26]  # add terminator

def encode_to_tiles(s):
    v = to_values(s)
    bits = ''.join(f'{x:05b}' for x in v)
    n = int(bits, 2)
    tiles = to_base224(n)
    return tiles

def decode_from_tiles(tiles): 
    n = from_base224(tiles)
    bits = bin(n)[2:]
    pad = (-len(bits)) % 5
    bits = '0'*pad + bits

    out = []
    for i in range(0, len(bits), 5): 
        val = int(bits[i:i+5], 2)
        if val != 26: 
            out.append(val_to_char[val])
    return ''.join(out)

s = "you suck at this game"
tiles = encode_to_tiles(s)
print("String: " + s)
print(f"Tiles: {tiles}")
print("Decoded string: " + s)
