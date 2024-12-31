"""
This class will be used for file handling, 
mainly for writing into files and reading from files
"""

class FileHandler:
    
    @staticmethod
    def read_from_file(file_path):
        try:
            with open(file_path, 'r') as file:
                data = file.read()
            return data
        except IOError as e:
            print(f"Error reading file {file_path}: {e}")
            return ""
    


    @staticmethod
    def write_to_file(file_path, data):
        try:
            with open(file_path, 'w') as file:
                file.write(data)
            print(f"Data written to {file_path}")
        except IOError as e:
            print(f"Error writing to file {file_path}: {e}")
        