import requests

char_stack = []

char_map = {
    0: 'A',
    1: 'B',
    2: 'C',
    3: 'D',
    4: 'E',
    5: 'F',
    6: 'G',
    7: 'H',
    8: 'I',
    9: 'J',
    10: 'K',
    11: 'L',
    12: 'M',
    13: 'N',
    14: 'O',
    15: 'P',
    16: 'Q',
    17: 'R',
    18: 'S',
    19: 'T',
    20: 'U',
    21: 'V',
    22: 'W',
    23: 'X',
    24: 'Y',
    25: 'Z',
    26: ' ',
    27: '.',
    28: ',',
    29: '!',
    30: '?',
    31: ']',
}



def add_bits(message):
    global char_stack
    for bit in message:
        char_stack.append(int(bit))
    check_complete_char()


def check_complete_char():
    global char_stack
    while len(char_stack) >= 5:
        byte_bits = char_stack[:5]
        char_stack = char_stack[5:]
        byte_value = 0
        for bit in byte_bits:
            byte_value = (byte_value << 1) | bit
        print(f"Received byte: {byte_value} ('{chr(byte_value)}')")

        BASE_URL = "http://127.0.0.1:5000/newchar"  # change if Flask runs elsewhere

        char = char_map.get(byte_value, '')  # default to '' for unknown
        url = f"{BASE_URL}/{char}"
        try:
            res = requests.get(url)
            if res.ok:
                print(f"Sent char: {char}")
            else:
                print(f"Failed to send {char}: {res.status_code}")
        except Exception as e:
            print("Error:", e)
    