from Token import *
from SlidingWindow import *

class LZ77Compressor():
    """
    This class is used as an interface for the LZ77 algorithm compressor
    We will implement the following
    - compress
    - decompress
    - calculate size in bits
    """
    
    def __init__(self, window_size: int = 10, look_ahead_buffer_size: int = 5):
    
        # Setting up sliding window config
        self.search_buffer_size = window_size - look_ahead_buffer_size # Where we will search for the patterns already encoded
        self.look_ahead_buffer_size = look_ahead_buffer_size
        self.window = SlidingWindow(self.search_buffer_size, self.look_ahead_buffer_size)

    def compress(self, data : str) -> list:
        tokens = [] # this is where we store tokens or tags
        position = 0 # Current position we are in
        self.window.search_buffer.clear() # we clear the buffer so if we tried other
        # examples it would still work

        while position < len(data): 

            offset, length, next_symbol = self.window.find_longest_match(data, position) # find longest match 
            # what find longest match do is find the tuble we will use for tokenizatino
            tokens.append(Token(offset, length, next_symbol))

            steps_to_move = (1 + length)
            
            for _ in range(steps_to_move):
                if position < len(data):
                    self.window.slide_forward(data[position]) # adds new charater to the sliding window
                    position += 1 

        return tokens


    def decompress(self, tokens: list) -> str:
        decompressed_data = []

        for token in tokens:
            if token.offset > 0:
                start = len(decompressed_data) - token.offset
                for i in range(token.length):
                    decompressed_data.append(decompressed_data[start + i])
            
            decompressed_data.append(token.next_symbol)

        return ''.join(decompressed_data)
    

    def calculate_sizes(self, data: str, tokens: list, offset_bits=5, length_bits=5, symbol_bits=8) -> tuple:
        original_size = len(data) * symbol_bits

        compressed_size = 0
        for token in tokens:
            compressed_size += offset_bits + length_bits + symbol_bits

        return original_size, compressed_size