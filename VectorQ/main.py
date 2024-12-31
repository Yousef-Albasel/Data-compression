from VQ import *

vq = VectorQuantizer()
vq.compress('Images/cat.jpg', block_size=2, codebook_size=32)
reconstructed_image = vq.reconstruct_image()
vq.display_results("Images/cat.jpg")
vq.save_image("Images/output/poor_cat.jpg")