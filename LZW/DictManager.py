class DictManager:
    def __init__(self, offset: int, decompress_mode: bool = 0):
        # Flag initiates the input as decompress mode or not
        if decompress_mode:
            self.dictionary = {i: chr(i) for i in range(offset + 1)}
        else:
            self.dictionary = {chr(i): i for i in range(offset + 1)}
        self.next = offset + 1

    def get_code(self, code):
        return self.dictionary.get(code, -1)
    
    def add_code(self, code): # add for compress
        if code not in self.dictionary:
            self.dictionary[code] = self.next
            self.next += 1

    def add_entry(self, entry): # add for decompress
        if self.next not in self.dictionary:
            self.dictionary[self.next] = entry
            self.next += 1

    def display(self):
        for code, value in self.dictionary.items():
            print(f"{code}: {value}")
