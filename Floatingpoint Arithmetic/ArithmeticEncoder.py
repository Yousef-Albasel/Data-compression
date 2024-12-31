from FileHandler import *
import struct

class ArithmeticEncoder:
    def __init__(self):
        self.probabilities = dict()
        self.ranges = dict()
    
    def compress(self, path):
        data = FileHandler.read_from_file(path)
        if not data:
            print("No data to compress.")
            return
        self.calculate_ranges(data)
        
        lower,upper = self.ranges[data[0]]
        
        for symbol in data[1:]:
            low, high = self.ranges[symbol]
            range_width = upper - lower
            upper = lower + range_width * high
            lower = lower + range_width * low
            if (symbol != data[-1]):
                print("New Lower Bound:", lower)
                print("New Upper Bound:", upper)
        print("Final Lower Bound:", lower)
        print("Final Upper Bound:", upper)
        compressed_value = (lower + upper) / 2

        serialized_probabilities = self.serialize_dict(self.probabilities)
        
        FileHandler.write_to_file("compressed_data.txt", str(compressed_value) + "," + serialized_probabilities + "," + str(len(data)))
        print("Compression completed.")
    
    def decompress(self, path):
        self.ranges = {}
        self.probabilities = {}
        compressed_file = FileHandler.read_from_file(path)
        compressed_data = compressed_file.split(',')
        print (compressed_data)

        value = float(compressed_data[0])
        self.probabilities = self.unserialize_dict(compressed_data[1])
        length = int(compressed_data[2])
        print (value)
        print (self.probabilities)
        print (length)
        # recalculate ranges
        cumulative = 0.0
        for symbol, prob in (self.probabilities.items()):
            low = cumulative
            high = cumulative + prob
            self.ranges[symbol] = (low, high)
            cumulative = high
        
        print("Ranges:", self.ranges)
        print (self.ranges)
            
        decompressed_string = ""
        symbol = self.find_symbol(value)
        lower,upper = self.ranges[symbol]
        for i in range(length):
            print (value)
            decompressed_string += symbol
            value = (value - lower) / (upper - lower)
            symbol = self.find_symbol(value)
            low, high = self.ranges[symbol]
            range_width = upper - lower
            upper = lower + range_width * high
            lower = lower + range_width * low

        print(decompressed_string)
        FileHandler.write_to_file("Decompressed_data.txt",decompressed_string)

    def serialize_dict(self, dictionary):
        return ';'.join(f"{key}:{value}" for key, value in dictionary.items())
    
    def unserialize_dict(self, serialized_dict):
        return {key: float(value) for key, value in (item.split(':') for item in serialized_dict.split(';'))}
  
    def find_symbol(self, value):
        for symbol, (low, high) in self.ranges.items():
            if low <= value < high:
                return symbol
        return None
            
    def calculate_ranges(self, data):
        frequency = {}
        for symbol in data:
            frequency[symbol] = frequency.get(symbol, 0) + 1
        
        total_symbols = sum(frequency.values())
        self.probabilities = {symbol: freq / total_symbols for symbol, freq in frequency.items()}
        print("Probabilities:", self.probabilities)

        cumulative = 0.0
        for symbol, prob in (self.probabilities.items()):
            low = cumulative
            high = cumulative + prob
            self.ranges[symbol] = (low, high)
            cumulative = high
        
        print("Ranges:", self.ranges)
