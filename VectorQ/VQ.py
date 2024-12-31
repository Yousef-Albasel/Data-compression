import math
from PIL import Image
import matplotlib.pyplot as plt
import random
from util import *
class VectorQuantizer:
    def __init__(self):
        self.codebook = []
        self.image_vectors = []
        self.vector_labels = []
        self.original_shape = None
        self.block_size = None
        self.codebook_size = None
        self.saved_image = None

    def compress(self, image_path, block_size, codebook_size):
        image = Image.open(image_path).convert("L")
        width, height = image.size
        self.original_shape = (width, height)
        self.block_size = block_size
        self.codebook_size = codebook_size
        pixel_matrix = convert_to_matrix(image, width, height)
        self.image_vectors = get_image_vectors(pixel_matrix, block_size, width, height)
        self.codebook = lbg(self.image_vectors, codebook_size,block_size)
        self.vector_labels = [find_nearest(vector, self.codebook) for vector in self.image_vectors]
        self.save_to_file("compressed_image.txt")


    def reconstruct_image(self,filename="compressed_image.txt"):
        self.load_from_file(filename)
        if not self.codebook or not self.vector_labels:
            raise ValueError("No codebook or labels available.")
        
        width, height = self.original_shape
        blocks_per_row = width // self.block_size
        reconstructed = Image.new("L", self.original_shape)
        pixels = reconstructed.load()
        
        for idx, label in enumerate(self.vector_labels):
            # retrieve a block
            block = self.codebook[label] # - > block = codebook[35]
            block_row = (idx // blocks_per_row) * self.block_size # index for this block (ex 10th label and block 2x2)
                                                                  # 
            block_col = (idx % blocks_per_row) * self.block_size
            
            for i, row in enumerate(block):
                for j, pixel in enumerate(row):
                    pixels[block_col + j, block_row + i] = int(pixel)
        self.saved_image = reconstructed;
        return reconstructed

    def display_results(self, original_image_path):
        original_image = Image.open(original_image_path).convert("L")
        reconstructed_image = self.reconstruct_image()
        
        fig, (ax1, ax2) = plt.subplots(1, 2)
        ax1.imshow(original_image, cmap='gray')
        ax1.set_title('Original Image')
        ax2.imshow(reconstructed_image, cmap='gray')
        ax2.set_title('Reconstructed Image')
        plt.show()

    def save_image(self,filename):
        self.saved_image.save(filename)

    def save_to_file(self, filename):
        with open(filename, 'w') as file:
            file.write(f"Block Size: {self.block_size}\n")
            file.write(f"Codebook Size: {self.codebook_size}\n")

            file.write("Codebook:\n")
            for code in self.codebook:
                flat_code = flatten_block(code)
                file.write(" ".join(map(str, flat_code)) + "\n")
            
            file.write("Vector Labels:\n")
            file.write(" ".join(map(str, self.vector_labels)) + "\n")

    def load_from_file(self, filename):
        with open(filename, 'r') as file:
            self.block_size = int(file.readline().strip().split(": ")[1])
            self.codebook_size = int(file.readline().strip().split(": ")[1])
            
            line = file.readline().strip()
            self.codebook = []
            while True:
                line = file.readline().strip()
                if line == "Vector Labels:":
                    break
                flat_code = list(map(int, line.split()))
                block = unflatten_block(flat_code, self.block_size)
                self.codebook.append(block)

            labels_line = file.readline().strip()
            self.vector_labels = list(map(int, labels_line.split()))