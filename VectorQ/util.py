import math
from PIL import Image
from math import ceil,log2

# 160 -> log2(160) = 7 , 2^8
def next_power_of_two(n):
    return 2 ** ceil(log2(n))

def pad_matrix(matrix, padded_width, padded_height):
    current_height = len(matrix)
    current_width = len(matrix[0])

    for row in matrix:
        row.extend([0] * (padded_width - current_width)) # add 0 to current row
    for _ in range(padded_height - current_height): # add rows of zeros 
        matrix.append([0] * padded_width)

def convert_to_matrix(image, width, height) -> list:
    pixel_matrix = [[image.getpixel((x, y)) for x in range(width)] for y in range(height)]
    padded_width = next_power_of_two(width)
    padded_height = next_power_of_two(height)
    pad_matrix(pixel_matrix, padded_width, padded_height)
    return pixel_matrix


def get_image_vectors(pixel_matrix, block_size, width, height):
    image_vectors = []
    for i in range(0, height - block_size + 1, block_size):
        for j in range(0, width - block_size + 1, block_size):
            block = []
            for y in range(block_size):
                row = []
                for x in range(block_size):
                    row.append(pixel_matrix[i + y][j + x])
                block.append(row)
            image_vectors.append(block)
    return image_vectors


def flatten_block(block): # from 2D to 1D
    flat_list = []
    for row in block:
        for pixel in row:
            flat_list.append(pixel)
    return flat_list

def unflatten_block(vector, block_size): # from 1D to 2D
    block = []
    for i in range(0, len(vector), block_size):
        row = []
        for j in range(block_size):
            row.append(vector[i + j])
        block.append(row)
    return block

def mean_vector(vectors):
    if not vectors:
        raise ValueError("vectors can't be empty")
    flattened_vectors = [flatten_block(v) for v in vectors]
    """
    [[1,2],[3,4]] - > [1,2,3,4]
    flattened_vectors is 2D
    [[1,2,3,4],
     [5,6,7,8],
     [0,5,2,6]]
        
    """
    return [round(sum(x)/len(x)) for x in zip(*flattened_vectors)] 

def distance(vector1, vector2):
    flat1 = flatten_block(vector1)
    flat2 = flatten_block(vector2)
    return math.sqrt(sum((a - b) ** 2 for a, b in zip(flat1, flat2)))

def find_nearest(vector, codebook):
    distances = [distance(vector, code) for code in codebook] # call on all vectors
    return distances.index(min(distances)) # decide which is nearest code for this vector

def lbg(image_vectors, codebook_size, block_size):
    codebook = [unflatten_block(mean_vector(image_vectors), block_size)]
    
    while len(codebook) < codebook_size:
        new_codebook = []
        # Split the vector 
        for code in codebook:
            flat_code = flatten_block(code)
            code1 = [max(0, min(255, x + 1)) for x in flat_code]
            code2 = [max(0, min(255, x - 1)) for x in flat_code]

            new_codebook.extend([unflatten_block(code1, block_size), 
                               unflatten_block(code2, block_size)])
        
        # if number of codebooks generated exceeded the size
        codebook = new_codebook[:codebook_size]

        # get best K vectors
        for _ in range(150):
            association_matrix = [[] for _ in range(len(codebook))]
            """
            eg. based on indices
            0 - > [[1,2,3,4],[5,6,7,8]]
            1 - >[[5,7,8,3],[2,5,7,8]]

            """

            # Associate
            for vector in image_vectors:
                nearest = find_nearest(vector, codebook)
                association_matrix[nearest].append(vector)
            
            # Calculate mean for these
            new_codebook = []
            for vectors in association_matrix:
                if vectors:
                    new_code = unflatten_block(mean_vector(vectors), block_size)
                    new_codebook.append(new_code)
                else:
                    new_codebook.append(codebook[len(new_codebook)])
            
            all_converged = True
            for c1, c2 in zip(codebook, new_codebook):
                if distance(c1, c2) != 0:
                    all_converged = False
                    break

            if all_converged:
                break
                
            codebook = new_codebook
            
    return codebook

