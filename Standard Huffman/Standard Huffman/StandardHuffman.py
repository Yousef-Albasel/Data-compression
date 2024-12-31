from FileHandler import *
import heapq
import json
class StandardHuffman:
    def __init__(self):
        self.frequency = {}
        self.heap = []
        self.codes = {}
    def compress(self, path):
        uncompressed_string = FileHandler.read_from_file(path)
        for symbol in uncompressed_string:
            if symbol in self.frequency:
                self.frequency[symbol] += 1
            else:
                self.frequency[symbol] = 1
        # pushing symbols and frequncies into the heap
        self.build_heap(self.frequency)
        # finding least frequencies and adding 
        self.build_tree(self.heap)
        # assign codes
        _,self.root = self.heap[0]
        self.assign_codes(self.root, "")


        encoded_string = ''.join(self.codes[symbol] for symbol in uncompressed_string)
        frequency_table_json = self.serialize_frequency_table()
        
        output_data = f"{frequency_table_json}\n{encoded_string}"
        FileHandler.write_to_file("output.txt", output_data)

    def decompress(self,path):
        self.heap = []
        self.codes = {}
        with open(path, "r") as f:
            lines = f.readlines()
    
        frequency_table_string = lines[0].strip()
        encoded_string = ''.join(lines[1:]).strip()
        self.frequency = self.deserialize_frequency_table(frequency_table_string)

        self.build_heap(self.frequency)
        self.build_tree(self.heap)
        _,self.root = self.heap[0]
        self.assign_codes(self.root, "")
        reversed_codes = {code: symbol for symbol, code in self.codes.items()}
        
        current_code = ""
        decoded_string = ""
        
        for bit in encoded_string:
            current_code += bit
            if current_code in reversed_codes:
                decoded_string += reversed_codes[current_code]
                current_code = ""
        
        FileHandler.write_to_file("decoded_output.txt",decoded_string)    
    def assign_codes(self, node, code):
        if isinstance(node,str):
            self.codes[node] = code
        else:
            left, right = node
            self.assign_codes(left, code + "0")
            self.assign_codes(right, code + "1")

        
    def serialize_frequency_table(self):
        serialized = ""
        for symbol, freq in self.frequency.items():
            serialized += f"{symbol}{freq}"
        return serialized

    def deserialize_frequency_table(self,data):
        frequency = {}
        i = 0
        while i < len(data):
            symbol = data[i]  # Read symbol
            i += 1
            freq = ""
            while i < len(data) and data[i].isdigit():  # Read frequency
                freq += data[i]
                i += 1
            frequency[symbol] = int(freq)
        return frequency
   
    def build_heap(self,frequencies):
        for symbol, freq in frequencies.items():
            heapq.heappush(self.heap, (freq, symbol))

    def build_tree(self,heap):
        while len(self.heap) > 1:
            left_freq, left_symbol = heapq.heappop(heap)
            right_freq, right_symbol = heapq.heappop(heap)
            heapq.heappush(heap, (left_freq + right_freq, (left_symbol, right_symbol)))
        
    def print_frequencies(self):
        for symbol, count in self.frequency.items():
            print(f"Symbol: {symbol}, Frequency: {count}")

    def print_heap(self):
        for symbol, count in self.heap:

            print(f"Frequency: {symbol}, Symbol: {count}")

    def print_codes(self):
        for symbol, code in self.codes.items():
            print(f"Symbol: {symbol}, Code: {code}")