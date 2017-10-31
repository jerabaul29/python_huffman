from __future__ import print_function
import pyhuffman.pyhuffman as pyhuffman
import os

"""
A test case, that can also be used as example, about the use of hashable elements
as symbols.
"""

path_to_here = os.path.dirname(os.path.realpath(__file__)) + '/'


def test_use_hashable():
    freq = [(0.25, 'aa'), (0.25, '\xFF'), (0.25, 1), (0.25, (1, 2))]

    path_to_list_frequencies = path_to_here + 'data_huffman_tree_hashable.pkl'
    binary_data = path_to_here + 'binary_data_test_hashable.bin'

    # build the Huffman tree, dictionary and reverse dictionary
    huffman_tree = pyhuffman.HuffmanTree(frequency_data=freq, path_to_tree=path_to_list_frequencies)

    # build the tree and encode ----
    data_test = ['aa', 'aa', 1, 1, 1, (1, 2), '\xFF']
    huffman_tree.encode_as_bitarray(data_test, path_to_save=binary_data)

    # build a new tree to decode (just to show how to restaure from saved data) ----
    huffman_tree_restaured = pyhuffman.HuffmanTree(path_to_tree=path_to_list_frequencies)
    decoded = huffman_tree_restaured.decode_from_bitarray(path_to_decode=binary_data)

    assert(decoded == data_test)

    os.remove(path_to_list_frequencies)
    os.remove(binary_data)
