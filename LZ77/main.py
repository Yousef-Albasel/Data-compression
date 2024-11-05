from LZ77Compressor import *

compressor = LZ77Compressor(window_size=22, look_ahead_buffer_size=5)

data = "Yousef Albasel"
print ("Original Data:", data)
tokens = compressor.compress(data)
print("Compressed tokens:", [(t.offset, t.length, t.next_symbol) for t in tokens])

decompressed_data = compressor.decompress(tokens)
print("Decompressed data:", decompressed_data)


data = "ABCABABC"
print ("Original Data:", data)
tokens = compressor.compress(data)
print("Compressed tokens:", [(t.offset, t.length, t.next_symbol) for t in tokens])

decompressed_data = compressor.decompress(tokens)
print("Decompressed data:", decompressed_data)

original_size, compressed_size = compressor.calculate_sizes(data, tokens)
print("Original size:", original_size)
print("Compressed sizes:", compressed_size)