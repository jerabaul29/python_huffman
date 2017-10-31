from __future__ import print_function
from bitarray import bitarray
import pyhuffman.pyhuffman as pyhuffman

"""
A test case that can also be used as example, about how to build trees.
"""


def test_valid_dicts():
    # example of data: frequencies in the alphabet for typical english text
    # this data is from: https://stackoverflow.com/questions/11587044/how-can-i-create-a-tree-for-huffman-encoding-and-decoding
    freq = [
        (8.167, 'a'), (1.492, 'b'), (2.782, 'c'), (4.253, 'd'),
        (12.702, 'e'), (2.228, 'f'), (2.015, 'g'), (6.094, 'h'),
        (6.966, 'i'), (0.153, 'j'), (0.747, 'k'), (4.025, 'l'),
        (2.406, 'm'), (6.749, 'n'), (7.507, 'o'), (1.929, 'p'),
        (0.095, 'q'), (5.987, 'r'), (6.327, 's'), (9.056, 't'),
        (2.758, 'u'), (1.037, 'v'), (2.365, 'w'), (0.150, 'x'),
        (1.974, 'y'), (0.074, 'z')]

    # build the Huffman tree, dictionary and reverse dictionary
    huffman_tree = pyhuffman.HuffmanTree(frequency_data=freq)

    assert len(huffman_tree.huffman_dict.keys()) == 26

    valid_dict = {'a': '1110',
                  'b': '110000',
                  'c': '01001',
                  'd': '11111',
                  'e': '100',
                  'f': '00100',
                  'g': '110011',
                  'h': '0110',
                  'i': '1011',
                  'j': '001011011',
                  'k': '0010111',
                  'l': '11110',
                  'm': '00111',
                  'n': '1010',
                  'o': '1101',
                  'p': '110001',
                  'q': '001011001',
                  'r': '0101',
                  's': '0111',
                  't': '000',
                  'u': '01000',
                  'v': '001010',
                  'w': '00110',
                  'x': '001011010',
                  'y': '110010',
                  'z': '001011000'}

    assert huffman_tree.huffman_dict == valid_dict

    valid_bitarray_tree_ = {'a': bitarray('1110'),
                            'b': bitarray('110000'),
                            'c': bitarray('01001'),
                            'd': bitarray('11111'),
                            'e': bitarray('100'),
                            'f': bitarray('00100'),
                            'g': bitarray('110011'),
                            'h': bitarray('0110'),
                            'i': bitarray('1011'),
                            'j': bitarray('001011011'),
                            'k': bitarray('0010111'),
                            'l': bitarray('11110'),
                            'm': bitarray('00111'),
                            'n': bitarray('1010'),
                            'o': bitarray('1101'),
                            'p': bitarray('110001'),
                            'q': bitarray('001011001'),
                            'r': bitarray('0101'),
                            's': bitarray('0111'),
                            't': bitarray('000'),
                            'u': bitarray('01000'),
                            'v': bitarray('001010'),
                            'w': bitarray('00110'),
                            'x': bitarray('001011010'),
                            'y': bitarray('110010'),
                            'z': bitarray('001011000')}

    assert huffman_tree.bitarray_dict == valid_bitarray_tree_

test_valid_dicts()
