# pyhuffman

This is a pure Python implementation of Huffman tree, based on the answer provided here (I was not the author of neither the post nor the answer):

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

## Releases

- 1.1: correcting trailing zeros bugs
- 1.0: initial release

## Features

- Generate / load / save to disk Huffman trees.
- Encode / decode / load / save to disk iterables using a Huffman tree.
- Iterables can be strings, but also iterables composed of any sort of hashable data (so that it can be used as keys of a dictionary), for example lists, your own objects, pairs of characters, words, etc.
- Take care of trailing zeros in last byte if the data length is not a multiple of 8 bits.

## Tests and examples

Tests can be run from the repository root running:

```
pytest -v .
```

Tests can also be used as examples.

The module can be used to generate Huffman trees:

```Python
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

Produces:

```
{'!': bitarray('01001111'), ' ': bitarray('0001'), ',': bitarray('1110010'), 'a': bitarray('1110'), 'c': bitarray('01001'), 'b': bitarray('110000'), 'e': bitarray('100'), 'd': bitarray('11111'), 'g': bitarray('110011'), 'f': bitarray('00100'), 'i': bitarray('1011'), 'h': bitarray('0110'), 'k': bitarray('0010111'), 'j': bitarray('001011011'), 'm': bitarray('00111'), 'l': bitarray('11110'), 'o': bitarray('1101'), 'n': bitarray('1010'), 'q': bitarray('001011001'), 'p': bitarray('110001'), 's': bitarray('0111'), 'r': bitarray('0101'), 'u': bitarray('01000'), 't': bitarray('000'), 'w': bitarray('00110'), 'v': bitarray('001010'), 'y': bitarray('110010'), 'x': bitarray('001011010'), 'z': bitarray('001011000')}
```

Those trees can then be used to decode / encode data. Reading and writing to binary files is also supported.

```Python
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
huffman_tree = pyhuffman.HuffmanTree(frequency_data=freq, path_to_tree=path_to_list_frequencies)
huffman_tree.encode_as_bitarray(data, path_to_save=binary_file)

# build a new tree to decode (just to show how to restaure from saved data) ----
huffman_tree_restaured = pyhuffman.HuffmanTree(path_to_tree=path_to_list_frequencies)
decoded = ''.join(huffman_tree_restaured.decode_from_bitarray(path_to_decode=binary_file))

print(decoded)
```

Produces:

```
this is a short string, but of course the encoding could work as well for any other type and length of data!
```

Note that the Huffman encoding can be used on any hashable object (so, tuples or your own objects for example, but not lists):

```python
from __future__ import print_function
import pyhuffman.pyhuffman as pyhuffman

freq = [(0.25, 'aa'), (0.25, '\xFF'), (0.25, 1), (0.25, (1, 2))]

path_to_list_frequencies = 'data_huffman_tree.pkl'
binary_data =  'binary_data_test.bin'

# build the Huffman tree, dictionary and reverse dictionary
huffman_tree = pyhuffman.HuffmanTree(frequency_data=freq, path_to_tree=path_to_list_frequencies)

# build the tree and encode ----
data_test = ['aa', 'aa', 1, 1, 1, (1, 2), '\xFF']
huffman_tree.encode_as_bitarray(data_test, path_to_save=binary_data)

# build a new tree to decode (just to show how to restaure from saved data) ----
huffman_tree_restaured = pyhuffman.HuffmanTree(path_to_tree=path_to_list_frequencies)
decoded = huffman_tree_restaured.decode_from_bitarray(path_to_decode=binary_data)

print(decoded)
```

Produces:

```
['aa', 'aa', 1, 1, 1, (1, 2), '\xff']
```

For more detailed examples of how to use the module, look at the tests (**test/test_example_build_tree.py** and **test/test_example_encode_hamlet.py**). In particular, you will find a few helper functions to build the frequency list adapted to any input file in **test/test_example_encode_hamlet.py** .
