"""
Class LZWCompressor for handling the compress/decompress operations
Author : Yousef Albasel
"""

from DictManager import DictManager
from FileHandler import FileHandler

class LZWCompressor:
    def __init__(self):
        self.dict_manager = DictManager(127)

    def compress(self, input_file):
        self.uncompressed_data = FileHandler.read_from_file(input_file)
        compressed_data = []  # store compressed
        current_sequence = ""
        # Example : A BAABABBAABAABAAAABABBBBB
        for char in self.uncompressed_data: # A
            combined_sequence = current_sequence + char # A 

            if self.dict_manager.get_code(combined_sequence) != -1: # True
                current_sequence = combined_sequence # extend 
            else:
                # In this case it will add whatever in the dictionary (nothing for now)
                compressed_data.append(self.dict_manager.get_code(current_sequence))

                self.dict_manager.add_code(combined_sequence)
                current_sequence = char

        # If leftover
        if current_sequence:
            compressed_data.append(self.dict_manager.get_code(current_sequence))

        # print(self.dict_manager.display())
        
        FileHandler.write_to_file(f"{input_file}_compressed.txt"," ".join(map(str, compressed_data)))
        print(f"Compressed data successfully!")


    def decompress(self, compressed_file):
        compressed_data = FileHandler.read_from_file(compressed_file).split()
        compressed_data = list(map(int, compressed_data))  # Convert to integers
        
        self.dict_manager = DictManager(127, 1)  # Reset for decompression mode

        # Decompression logic
        if not compressed_data:
            print("No data to decompress.")
            return ""

        # Start with the first code
        previous_code = compressed_data[0]
        output_string = self.dict_manager.get_code(previous_code)
        decompressed_data = [output_string]

        # Iterate over remaining codes
        for code in compressed_data[1:]:
            # Determine if the code exists in the dictionary
            if code in self.dict_manager.dictionary:
                entry = self.dict_manager.get_code(code)
            else:
                # Handle the special case where the code is missing
                entry = output_string + output_string[0]  

            # Append the entry to the decompressed data
            decompressed_data.append(entry)

            # Add the new sequence to the dictionary
            new_entry = output_string + entry[0]  
            self.dict_manager.add_entry(new_entry)

            # Update for the next iteration
            output_string = entry

        print (self.dict_manager.display())
        FileHandler.write_to_file(f"{compressed_file}_decompressed.txt", ''.join(decompressed_data))
        print(f"Decompressed data successfully!")
