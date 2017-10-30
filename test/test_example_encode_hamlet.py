from __future__ import print_function
import pyhuffman.pyhuffman as pyhuffman
import os

path_to_here = os.path.dirname(os.path.realpath(__file__)) + '/'
# path_to_here = ''

# functions for generating the frequency list ----


def generate_frequency_list(dict_appearances):
    """Generate the list to be used for building the Huffman tree from the
    dictionary of symbol appearances"""

    # total number of symbol appearances
    total_number_appearances = 0
    for key in dict_appearances:
        total_number_appearances += dict_appearances[key]

    frequency_list = []
    for key in dict_appearances:
        new_entry = (float(dict_appearances[key]) / total_number_appearances, key)
        frequency_list.append(new_entry)

    return frequency_list


def generate_frequency_dict(data):
    """Generate a dictionary of all symbols (keys) with their number of appearances
    (values) from data.
    """

    dict_appearances = {}

    for crrt_char in data:
        if crrt_char in dict_appearances:
            dict_appearances[crrt_char] += 1
        else:
            dict_appearances[crrt_char] = 1

    return dict_appearances


def generate_frequency_data(input_file):
    """Generate the frequency data to be used for building the Huffman tree.
    """

    dict_appearances = generate_frequency_dict(input_file)
    list_frequencies = generate_frequency_list(dict_appearances)

    return list_frequencies


def test_good_encoding_decoding():
    # various pathes ----
    # note: the raw text data for Hamlet comes from: https://www.gutenberg.org/cache/epub/1524/pg1524.txt
    path_to_hamlet = path_to_here + 'hamlet_from_gutember_project.txt'
    # where to save the list_frequencies to be able to re-build the same huffman tree
    path_to_list_frequencies = path_to_here + 'data_huffman_tree.pkl'
    # where to save the encoded output
    binary_hamlet_file = path_to_here + 'hamlet_huffman.bin'

    # generate list_frequencies ----
    with open(path_to_hamlet) as crrt_file:
        data_hamlet = crrt_file.read()

    list_frequencies = generate_frequency_data(data_hamlet)

    # build the tree and encode ----
    huffman_tree = pyhuffman.HuffmanTree(frequency_data=list_frequencies, path_to_tree=path_to_list_frequencies)
    huffman_tree.encode_as_bitarray(data_hamlet, path_to_save=binary_hamlet_file)

    # build a new tree to decode (just to show how to restaure from saved data) ----
    huffman_tree_restaured = pyhuffman.HuffmanTree(path_to_tree=path_to_list_frequencies)
    decoded = huffman_tree_restaured.decode_from_bitarray(path_to_decode=binary_hamlet_file)

    assert len(decoded) == 173940
    assert decoded[0: 10] == 'HAMLET, PR'
    assert decoded[-10:] == 'hot off.]\n'


def test_automatic_exhaustive_1():
    # various pathes ----
    # note: the raw text data for Hamlet comes from: https://www.gutenberg.org/cache/epub/1524/pg1524.txt
    path_to_hamlet = path_to_here + 'hamlet_from_gutember_project.txt'
    # where to save the list_frequencies to be able to re-build the same huffman tree
    path_to_list_frequencies = path_to_here + 'data_huffman_tree.pkl'
    # where to save the encoded output
    binary_hamlet_file = path_to_here + 'hamlet_huffman.bin'

    # generate list_frequencies ----
    with open(path_to_hamlet) as crrt_file:
        data_hamlet = crrt_file.read()

    list_frequencies = generate_frequency_data(data_hamlet)

    for stop in range(200, 230, 1):

        reduced_data = data_hamlet[100: stop]

        # build the tree and encode ----
        huffman_tree = pyhuffman.HuffmanTree(frequency_data=list_frequencies, path_to_tree=path_to_list_frequencies)
        huffman_tree.encode_as_bitarray(reduced_data, path_to_save=binary_hamlet_file)

        # build a new tree to decode (just to show how to restaure from saved data) ----
        huffman_tree_restaured = pyhuffman.HuffmanTree(path_to_tree=path_to_list_frequencies)
        decoded = huffman_tree_restaured.decode_from_bitarray(path_to_decode=binary_hamlet_file)

        assert(decoded == reduced_data)
