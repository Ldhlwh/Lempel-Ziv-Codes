import sys
import math
from bitarray import bitarray

class LZ77:
    def __init__(self, s, window_size=20):
        self.s = s
        self.window_size = window_size
        self.lookahead_buffer_size = 15
    
    def encode(self):
        MAX_LEN = len(self.s)
        i = 0
        output_buffer = bitarray(endian='big')
        
        while i < MAX_LEN:
            match = self.findLongestMatch(i)
            
            if match:
                (bestMatchDistance, bestMatchLength) = match
                
                output_buffer.append(True)
                output_buffer.frombytes(bytes([bestMatchDistance >> 4]))
                output_buffer.frombytes(bytes([((bestMatchDistance & 0xf) << 4) | bestMatchLength]))
                
                i += bestMatchLength
                
            else:
                output_buffer.append(False)
                output_buffer.frombytes(bytes([s[i]]))
                
                i += 1
                
        output_buffer.fill()
        return output_buffer
    def decode(self):
        output_buffer = []
        while len(s) >= 9:
            flag = s.pop(0)
            
            if not flag:
                byte = s[0:8].tobytes()
                
                output_buffer.append(byte)
                del s[0:8]
            else:
                byte1 = ord(s[0:8].tobytes())
                byte2 = ord(s[8:16].tobytes())
                
                del s[0:16]
                distance = (byte1 << 4) | (byte2 >> 4)
                length = (byte2 & 0xf)
                
                for i in range(length):
                    output_buffer.append(output_buffer[-distance])
        out_s = b''.join(output_buffer)
        
        return out_s
    
    def findLongestMatch(self, current_position):
        end_of_buffer = min(current_position + self.lookahead_buffer_size, len(s) + 1)
        
        best_match_distance = -1
        best_match_length = -1
        
        for j in range(current_position + 2, end_of_buffer):
            start_index = max(0, current_position - self.window_size)
            substring = s[current_position:j]
            
            for i in range(start_index, current_position):
                repetitions = len(substring) // (current_position - i)
                last = len(substring) % (current_position - i)
                matched_string = s[i:current_position] * repetitions + s[i:i+last]
                
                if matched_string == substring and len(substring) > best_match_length:
                    best_match_distance = current_position - i
                    best_match_length = len(substring)
        if best_match_distance > 0 and best_match_length > 0:
            return (best_match_distance, best_match_length)
        return None

if __name__ == '__main__':
    s = bitarray(endian='big')
    with open('Introduction to Data Compression.txt', 'rb') as input_file:
        s = input_file.read()
    encoder = LZ77(s)
    inner_code = encoder.encode()
    print(len(inner_code) / len(s))
    #print(inner_code)
    s = inner_code
    new_s = encoder.decode()
    with open('test_LZ77.txt', 'wb') as output_file:
        output_file.write(new_s)
