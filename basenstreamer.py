from typing import List, Optional

from message_handler import *

class ChunkerStreamer:
    def __init__(self):
        self.incoming_binary_string = ""

    @staticmethod
    def chunk_binary(binstr: str):
        chunks = []
        while len(binstr) > 0:
            print(binstr)
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
        if val < 128:
            binary_val = bin(val)[2:].zfill(7)
        else:
            binary_val = bin(val)[2:].zfill(8)

        self.incoming_binary_string += str(binary_val)

    def pop_all(self) -> Optional[str]:
        """Returns all available string if there is any, None if not"""

        num_chars = len(self.incoming_binary_string)//5
        if num_chars == 0:
            return None
        result = ""
        for i in range(num_chars):
            binary_char = self.incoming_binary_string[i*5:(i+1)*5]
            result += char_map[int(binary_char, 2)]
        self.incoming_binary_string = self.incoming_binary_string[num_chars*5:]
        return result

        
