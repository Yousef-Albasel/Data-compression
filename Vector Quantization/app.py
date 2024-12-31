from VectorQuantizer import *

vq = VectorQuantizer()
block_size = 8
codebook_size = 64
vq.compress("abdullah (1).jpg", block_size, codebook_size)
decompressed_image = vq.decompress(block_size)
vq.show(decompressed_image)