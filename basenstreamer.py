from typing import List, Optional

def highest_set_bit(v: int) -> int:
    if v < 0:
        raise ValueError("Input must be a non-negative integer.")

    if v == 0:
        return -1
    
    return v.bit_length() - 1

def lowest_set_bit(v : int) -> int:
    i = 0
    if v == 0:
        return -1
    
    lsb_value = v & -v
    
    return lsb_value.bit_length() - 1

def to_base_n(value: int, base: int) -> list[int]:
    if base < 2:
        raise ValueError("Base must be an integer of 2 or greater.")
    if value < 0:
        raise ValueError("Value must be non-negative.")

    if value == 0:
        return [0]

    digits = []
    current_value = value
    
    while current_value > 0:
        remainder = current_value % base
        digits.append(remainder) 
        current_value //= base

    return digits

def from_base_n(digits: list[int], base: int) -> int:
    if base < 2:
        raise ValueError("Base must be an integer of 2 or greater.")
    if not all(0 <= d < base for d in digits):
        raise ValueError("All digits must be less than the base.")

    result = 0
    
    for i, digit in enumerate(digits):
        exponent = i
        result += digit * (base ** exponent)

    return result


import math
from typing import Optional

class baseNBinaryStreamer:
    offset : int = 0
    num : int = 0
    base : int = 0
    curr : int = 0

    def __init__(self, base):
        self.base = base

    def push(self, val : int):
        self.num += (val * (self.base ** self.curr))
        self.curr += 1

    def get_highest_safe_bit(self):
        return lowest_set_bit(self.base ** self.curr) - self.offset

    def pop_n(self, n : int):
        val = (self.num & (((1 << n) - 1) << self.offset)) >> self.offset
        self.offset += n
        return val
    
    def read_all(self, stride : int):
        return [(self.num & (((1 << stride) - 1) << o)) >> o for o in range(0,highest_set_bit(self.num), stride)]
    
    def read_all_past_curr(self, stride : int):
        return [(self.num & (((1 << stride) - 1) << o)) >> o for o in range(self.offset,highest_set_bit(self.num), stride)]

class chunkerStreamer:
    chunks : List[int] = []

    @staticmethod
    def chunk_binary(binstr: str):
        index = 0
        chunks = []
        while len(binstr) > 0:
            if len(binstr) >= 8:
                to_try_str = binstr[0:8]
                to_try = int(to_try_str, 2)
                if 224 >to_try >= 128:
                    chunks.append(to_try)
                    binstr = binstr[8:]
                else:
                    chunks.append(int(to_try_str[:-1], 2))
                    binstr = binstr[7:]
            elif len(binstr) == 7:
                chunks.append(int(binstr, 2))
                binstr = ""
            else:
                binstr = binstr.ljust(7, "0")
                chunks.append(int(binstr, 2))
                binstr = ""


        return chunks
    
    def push(self, val):
        self.chunks.append(val)

        
