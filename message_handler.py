import requests

char_stack = []

char_map = {
    0: 'a',
    1: 'b',
    2: 'c',
    3: 'd',
    4: 'e',
    5: 'f',
    6: 'g',
    7: 'h',
    8: 'i',
    9: 'j',
    10: 'k',
    11: 'l',
    12: 'm',
    13: 'n',
    14: 'o',
    15: 'p',
    16: 'q',
    17: 'r',
    18: 's',
    19: 't',
    20: 'u',
    21: 'v',
    22: 'w',
    23: 'x',
    24: 'y',
    25: 'z',
    26: ' ',
    27: '.',
    28: ',',
    29: '!',
    30: '?',
    31: ']',
}



# def add_bits(message):
#     global char_stack
#     for bit in message:
#         char_stack.append(int(bit))
#     check_complete_char()
#
#
# def check_complete_char():
#     global char_stack
#     while len(char_stack) >= 5:
#         byte_bits = char_stack[:5]
#         char_stack = char_stack[5:]
#         byte_value = 0
#         for bit in byte_bits:
#             byte_value = (byte_value << 1) | bit
#         print(f"Received byte: {byte_value} ('{chr(byte_value)}')")
#
#         BASE_URL = "http://127.0.0.1:5000/newchar"  # change if Flask runs elsewhere
#
#         char = char_map.get(byte_value, '')  # default to '' for unknown
#         url = f"{BASE_URL}/{char}"
#         try:
#             res = requests.get(url)
#             if res.ok:
#                 print(f"Sent char: {char}")
#             else:
#                 print(f"Failed to send {char}: {res.status_code}")
#         except Exception as e:
#             print("Error:", e)
    