import math
from PIL import Image
import matplotlib.pyplot as plt
import random

class VectorQuantizer:
    def __init__(self):
        self.codebook = []
        self.image_vectors = []
        self.vector_indices = []
        self.original_shape = None

    def get_pixel_matrix(self, image):
        width, height = image.size
        pixel_matrix = []
        for y in range(height):
            row = []
            for x in range(width):
                row.append(image.getpixel((x, y)))
            pixel_matrix.append(row)
        return pixel_matrix

    def flatten_block(self, block):
        return [pixel for row in block for pixel in row]

    def unflatten_block(self, vector, block_size):
        block = []
        for i in range(block_size):
            row = []
            for j in range(block_size):
                row.append(vector[i * block_size + j])
            block.append(row)
        return block

    def compress(self, image_path, block_size, codebook_size):
        # Open the image and convert to grayscale
        image = Image.open(image_path).convert("L")
        pixel_matrix = self.get_pixel_matrix(image)
        height, width = len(pixel_matrix), len(pixel_matrix[0])
        self.original_shape = (height, width)

        # Extract blocks from the image
        for i in range(0, height - block_size + 1, block_size):
            for j in range(0, width - block_size + 1, block_size):
                block = []
                for y in range(block_size):
                    row = pixel_matrix[i + y][j:j + block_size]
                    block.append(row)
                self.image_vectors.append(self.flatten_block(block))

        # Initialize codebook with random vectors
        random_indices = random.sample(range(len(self.image_vectors)), codebook_size)
        self.codebook = [self.image_vectors[i][:] for i in random_indices]
        
        # Perform k-means clustering
        self.kmeans_clustering(codebook_size, max_iterations=100)

        # Find closest codebook vector for each image vector
        self.vector_indices = self.find_closest_codes()

    def euclidean_distance(self, vector1, vector2):
        return sum((a - b) ** 2 for a, b in zip(vector1, vector2)) ** 0.5

    def mean_vector(self, vectors):
        if not vectors:
            return None
        length = len(vectors[0])
        sums = [0] * length
        for vector in vectors:
            for i, value in enumerate(vector):
                sums[i] += value
        return [sum_val / len(vectors) for sum_val in sums]

    def vectors_equal(self, vec1, vec2, tolerance=1e-6):
        return all(abs(a - b) < tolerance for a, b in zip(vec1, vec2))

    def kmeans_clustering(self, codebook_size, max_iterations):
        for iteration in range(max_iterations):
            old_codebook = [code[:] for code in self.codebook]
            
            # Associate vectors with closest codebook entry
            clusters = [[] for _ in range(codebook_size)]
            for vector in self.image_vectors:
                distances = [self.euclidean_distance(vector, code) for code in self.codebook]
                closest = distances.index(min(distances))
                clusters[closest].append(vector)

            # Update codebook vectors
            for i in range(codebook_size):
                if clusters[i]:
                    new_code = self.mean_vector(clusters[i])
                    if new_code:
                        self.codebook[i] = new_code

            # Check for convergence
            if all(self.vectors_equal(old, new) for old, new in zip(old_codebook, self.codebook)):
                break

    def find_closest_codes(self):
        indices = []
        for vector in self.image_vectors:
            distances = [self.euclidean_distance(vector, code) for code in self.codebook]
            indices.append(distances.index(min(distances)))
        return indices

    def decompress(self, block_size):
        height, width = self.original_shape
        blocks_h = height // block_size
        blocks_w = width // block_size

        # Create empty image
        decompressed = [[0 for _ in range(width)] for _ in range(height)]

        # Reconstruct image block by block
        for idx, code_idx in enumerate(self.vector_indices):
            i = (idx // blocks_w) * block_size
            j = (idx % blocks_w) * block_size
            block = self.unflatten_block(self.codebook[code_idx], block_size)
            
            # Place block in the decompressed image
            for y in range(block_size):
                for x in range(block_size):
                    if i + y < height and j + x < width:
                        decompressed[i + y][j + x] = int(block[y][x])

        # Convert to PIL Image
        output_image = Image.new('L', (width, height))
        for y in range(height):
            for x in range(width):
                output_image.putpixel((x, y), decompressed[y][x])
        
        return output_image

    def show(self, image):
        plt.imshow(image, cmap='gray')
        plt.axis('off')
        plt.show()

