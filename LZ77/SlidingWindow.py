from collections import deque
class SlidingWindow():
    def __init__(self, search_buffer_size: int, look_ahead_buffer_size: int):
        self.search_buffer = deque(maxlen=search_buffer_size)
        self.look_ahead_buffer_size = look_ahead_buffer_size


    def find_longest_match(self, data: str, position: int) -> tuple:
        # 0 1 2 3  4 5 6  7 8 9 - -
        # A A B B (A A B) B B B B A
        #          ^
        #   SB               LB
        #   ^                     ^
        # start                  EOB
        end_of_buffer = min(position + self.look_ahead_buffer_size, len(data)) # end for Look ahead buff
        offset = 0 # initialize offset
        length = 0  # initialize length
            # if the position is beyond search buffer, limit it to our s.buffer window size
        for start in range(max(0, position - len(self.search_buffer)), position): # search in search buffer
            match_length = 0
            #            Not Exceed SB                     LookAhead Buffer           Data in Search Buffer
            while (match_length < end_of_buffer - position and data[start + match_length] == data[position + match_length]):
                match_length += 1 # Keep going until u find best match

            if match_length > length: # if found bigger than 0
                offset = position - start
                length = match_length

        if length > 0 and position + length < len(data): # return the results, champ
            return offset, length, data[position + length]
        return 0, 0, data[position] # if not found 
    
    def slide_forward(self, char: str):
        # Add new character to the search buffer (left slide)
        self.search_buffer.append(char)
    