# pyhuffman

This is a pure Python implementation of Huffman tree, based on the answer provided here: 

https://stackoverflow.com/questions/11587044/how-can-i-create-a-tree-for-huffman-encoding-and-decoding

## Requirements

You will first need to install the bitarray package.

```
pip install bitarray
```

The module can then be installed from pip:

```
pip install pyhuffman
```

## Tests and examples

Tests can be run from the repository root running:

```
pytest -v .
```

The module can be used to generate Huffman trees:

```
from __future__ import print_function
import pyhuffman.pyhuffman as pyhuffman

freq = [
    (8.167, 'a'), (1.492, 'b'), (2.782, 'c'), (4.253, 'd'),
    (12.702, 'e'), (2.228, 'f'), (2.015, 'g'), (6.094, 'h'),
    (6.966, 'i'), (0.153, 'j'), (0.747, 'k'), (4.025, 'l'),
    (2.406, 'm'), (6.749, 'n'), (7.507, 'o'), (1.929, 'p'),
    (0.095, 'q'), (5.987, 'r'), (6.327, 's'), (9.056, 't'),
    (2.758, 'u'), (1.037, 'v'), (2.365, 'w'), (0.150, 'x'),
    (1.974, 'y'), (0.074, 'z')]

# build the Huffman tree, dictionary and reverse dictionary
huffman_tree = pyhuffman.HuffmanTree(freq)

print(huffman_tree.bitarray_dict)
```

Those trees can then be used to decode / encode data. Reading and writing to binary files is also supported.

```
import pyhuffman.pyhuffman as pyhuffman

freq = [
    (8.167, 'a'), (1.492, 'b'), (2.782, 'c'), (4.253, 'd'),
    (12.702, 'e'), (2.228, 'f'), (2.015, 'g'), (6.094, 'h'),
    (6.966, 'i'), (0.153, 'j'), (0.747, 'k'), (4.025, 'l'),
    (2.406, 'm'), (6.749, 'n'), (7.507, 'o'), (1.929, 'p'),
    (0.095, 'q'), (5.987, 'r'), (6.327, 's'), (9.056, 't'),
    (2.758, 'u'), (1.037, 'v'), (2.365, 'w'), (0.150, 'x'),
    (1.974, 'y'), (0.074, 'z'), (5.000, ' '), (1.000, ','),
    (0.500, '!')]

# build the Huffman tree, dictionary and reverse dictionary
huffman_tree = pyhuffman.HuffmanTree(freq)

# where to save the list_frequencies to be able to re-build the same huffman tree
path_to_list_frequencies = 'data_huffman_tree.pkl'
# where to save the encoded output
binary_file = 'encoded_huffman.bin'

# generate list_frequencies ----
data = """this is a short string, but of course the encoding could work as well for any other type and length of data!"""

# build the tree and encode ----
huffman_tree = pyhuffman.HuffmanTree(frequency_data=freq, path_to_save=path_to_list_frequencies)
huffman_tree.encode_as_bitarray(data, path_to_save=binary_file)

# build a new tree to decode (just to show how to restaure from saved data) ----
huffman_tree_restaured = pyhuffman.HuffmanTree(path_to_save=path_to_list_frequencies)
decoded = huffman_tree_restaured.decode_from_bitarray(path_to_decode=binary_file)

print(decoded)
```

For more detailed examples of how to use the module, look at the tests (test/test_example_build_tree.py and test/test_example_encode_hamlet.py). In particular, you will find a few helper functions to build the frequency list adapted to any output file in test/test_example_encode_hamlet.py .
