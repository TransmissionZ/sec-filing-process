path_to_compressed = r"C:\Users\Martin\Desktop\test\0000891092-12-007249.txt.bz2"
import bz2
import os


if not os.path.exists(path_to_compressed):
    print("There is no file", path_to_compressed)
else:
    with open(path_to_compressed, 'rb') as f:
        d = f.read()
    decompressed_data_string = bz2.decompress(d).decode("utf-8")
    print(decompressed_data_string[0:100])
    
