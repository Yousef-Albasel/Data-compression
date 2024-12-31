from StandardHuffman import *

h=StandardHuffman()
h.compress("input.txt")
h.print_heap()
h.print_codes()

h.decompress("output.txt")