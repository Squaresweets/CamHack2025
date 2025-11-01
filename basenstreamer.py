from typing import List, Optional

def lowest_set_bit(v : int) -> int:
    i = 0
    while (1 << i) & v == 0:
        i += 1
    return i

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


class baseNBinaryStreamer:
    baseN_values : List[int]
    base : int

    def __init__(self, base):
        self.base = base;
        self.baseN_values = []

    def push(self, value : int):
        self.baseN_values.append(value)

    def get_highest_safe_bit(self) -> int:
        return lowest_set_bit(self.base ** len(self.baseN_values))
    

    def seek_n(self, n : int) -> Optional[int]:
        if n > self.get_highest_safe_bit():
            return None
        
        return from_base_n(self.baseN_values, self.base) & ((1 << n) - 1)
    

    def pop_n(self, n : int) -> Optional[int]:
        if n > self.get_highest_safe_bit():
            return None
        
        val = from_base_n(self.baseN_values, self.base) 
        seek_value = self.seek_n(n)

        val >>= n

        self.baseN_values = to_base_n(val, self.base)
        if len(self.baseN_values) == 1 and self.baseN_values[0] == 0:
            self.baseN_values.remove(0)

        return seek_value
    


            

        

        
