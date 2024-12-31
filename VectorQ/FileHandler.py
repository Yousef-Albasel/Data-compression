    def save_to_file(self, filename):
        with open(filename, 'w') as file:
            # Save codebook
            file.write("Codebook:\n")
            for code in self.codebook:
                flat_code = flatten_block(code)  # Flatten each code for easy writing
                file.write(" ".join(map(str, flat_code)) + "\n")
            
            # Save vector labels
            file.write("Vector Labels:\n")
            file.write(" ".join(map(str, self.vector_labels)) + "\n")