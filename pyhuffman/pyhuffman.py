"""
huffman encoding pure Python implementation. Adapted based on some code from:
https://stackoverflow.com/questions/11587044/how-can-i-create-a-tree-for-huffman-encoding-and-decoding

Using the in-built C++ functions from the bitarray module for encoding / decoding
of prefix codes.
"""

from __future__ import print_function
import Queue
from bitarray import bitarray
import pickle


def generate_reverse_dict(dict_in):
    """Generate the reverse dictionary: (value, key) out of (key, value).
    The values in dict_in must be unique.
    """
    return dict((v, k) for k, v in dict_in)


def create_tree(frequencies):
    """Create the huffman tree from the list [(frequency, symbol)]
    """
    p = Queue.PriorityQueue()

    # create a leaf node in the priority queue for each symbol
    for value in frequencies:
        p.put(value)

    # while there are still nodes left in the priority queue, build the huffman tree
    while p.qsize() > 1:
        l, r = p.get(), p.get()
        node = HuffmanNode(l, r)
        p.put((l[0] + r[0], node))

    return p.get()


def walk_tree(node, prefix="", code={}):
    """Walk down the huffman tree under node to capture the code for each symbol
    """

    # walk to left
    if isinstance(node[1].left[1], HuffmanNode):
        walk_tree(node[1].left, prefix + "0", code)
    else:
        code[node[1].left[1]] = prefix + "0"

    # walk to right
    if isinstance(node[1].right[1], HuffmanNode):
        walk_tree(node[1].right, prefix + "1", code)
    else:
        code[node[1].right[1]] = prefix + "1"

    return(code)


class HuffmanNode(object):
    """Class used for building the Huffman tree. Binary tree with one left and
    one right leaf.
    """
    def __init__(self, left=None, right=None):
        self.left = left
        self.right = right

    def children(self):
        return((self.left, self.right))


class HuffmanTree(object):
    """Class for building, and extracting the information from the Huffman tree
    associated with user input"""

    def __init__(self, frequency_data=None, path_to_save=None):
        """Initialyze the Huffman tree and builds all internal variables.

        If frequency_data is None and path_to_save is not None, load everything
        from path_to_save.

        If frequency_data is not None, load it and if path_to_save is not None,
        save everything for later use in path_to_save.

        frequency_data must be a list [(frequency, symbol)] or a pickled such
        list.
        """

        # note: in the case when path_to_save is used, only the huffman_dict is
        # actually saved. This means frequency_data and tree are lost. But this
        # is enough to perform encryption and decryption.

        if frequency_data is not None:
            self.frequency_data = frequency_data

            # prepare all internal data
            self.build_tree()
            self.build_dictionary()
            self.build_reverse_dictionary()
            self.generate_bitarray_dict()

            if path_to_save is not None:  # save all internal data

                dict_all_information = {}

                # dict_all_information['frequency_data'] = self.frequency_data
                # dict_all_information['tree'] = self.tree
                dict_all_information['huffman_dict'] = self.huffman_dict
                # dict_all_information['huffman_reverse_dict'] = self.huffman_reverse_dict
                # dict_all_information['bitarray_dict'] = self.bitarray_dict

                with open(path_to_save, 'wb') as f:
                    pickle.dump(dict_all_information, f, pickle.HIGHEST_PROTOCOL)

        elif path_to_save is not None:

            with open(path_to_save, 'rb') as f:  # load all internal data
                dict_all_information = pickle.load(f)

            # self.frequency_data = dict_all_information['frequency_data']
            # self.tree = dict_all_information['tree']
            self.huffman_dict = dict_all_information['huffman_dict']
            # self.huffman_reverse_dict = dict_all_information['huffman_reverse_dict']
            self.build_reverse_dictionary()
            # self.bitarray_dict = dict_all_information['bitarray_dict']
            self.generate_bitarray_dict()

        else:
            raise ValueError("You must give either frequency_data or path_to_save!")

    def build_tree(self):
        """Build the Huffman tree.
        """
        self.tree = create_tree(self.frequency_data)

    def build_dictionary(self):
        """Build the dictionary symbol to Huffman code.
        """
        self.huffman_dict = walk_tree(self.tree)

    def build_reverse_dictionary(self):
        """Build the dictionary Huffman code to symbol.
        """
        self.huffman_reverse_dict = generate_reverse_dict(self.huffman_dict.iteritems())

    def generate_bitarray_dict(self):
        """Generate a bitarray dict that can be used for coding / decoding.
        """

        self.bitarray_dict = {}

        for key in self.huffman_dict:
            self.bitarray_dict[key] = bitarray(self.huffman_dict[key])

    def encode_as_bitarray(self, to_encode, path_to_save=None):
        """Encode the data to_encode using the huffman tree. to_encode must
        consist of symbols that are part of the Huffman tree. If path_to_save
        is not None, will be used to save the bitarray in binary form
        """
        encoded = bitarray()
        encoded.encode(self.bitarray_dict, to_encode)

        if path_to_save is not None:
            with open(path_to_save, 'wb') as fh:
                encoded.tofile(fh)

        else:
            return encoded

    def decode_from_bitarray(self, to_decode=None, path_to_decode=None):
        """Decode to_decode using the Huffman tree. Use either to_decode
        (directly give the data), or path_to_decode (path to the file to
        decode).
        """

        if to_decode is None and path_to_decode is None:
            raise ValueError("""You must give either data (to_decode) or path
                              to data (path_to_decode)!""")

        if to_decode is not None and path_to_decode is not None:
            raise ValueError("""You cannot give both data (to_decode) and path
                              to data (path_to_decode)!""")

        if path_to_decode is not None:
            to_decode = bitarray()
            with open(path_to_decode, 'rb') as fh:
                to_decode.fromfile(fh)

        dec = bitarray(to_decode).decode(self.bitarray_dict)

        return(''.join(dec))
