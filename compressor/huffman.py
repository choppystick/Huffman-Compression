import heapq
from collections import Counter
from bitarray import bitarray


class HuffmanNode:
    def __init__(self, char, freq):
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None

    def __lt__(self, other):
        return self.freq < other.freq


def build_huffman_tree(frequency):
    heap = [HuffmanNode(char, freq) for char, freq in frequency.items()]
    heapq.heapify(heap)

    while len(heap) > 1:
        left = heapq.heappop(heap)
        right = heapq.heappop(heap)
        internal = HuffmanNode(None, left.freq + right.freq)
        internal.left = left
        internal.right = right
        heapq.heappush(heap, internal)

    return heap[0]


def build_huffman_codes(node, current_code="", codes={}):
    if node is None:
        return

    if node.char is not None:
        codes[node.char] = current_code
        return

    build_huffman_codes(node.left, current_code + "0", codes)
    build_huffman_codes(node.right, current_code + "1", codes)

    return codes


def serialize_tree(node):
    if node is None:
        return "2"  # Represent empty node
    if node.char is not None:
        return f"1{node.char}"  # Leaf node
    return f"0{serialize_tree(node.left)}{serialize_tree(node.right)}"  # Internal node


def deserialize_tree(data):
    def deserialize_helper(iterator):
        try:
            node_type = next(iterator)
            if node_type == '2':
                return None
            if node_type == '1':
                return HuffmanNode(next(iterator), 0)
            left = deserialize_helper(iterator)
            right = deserialize_helper(iterator)
            node = HuffmanNode(None, 0)
            node.left = left
            node.right = right
            return node
        except StopIteration:
            return None

    return deserialize_helper(iter(data))


def run_length_encode(text):
    encoded = []
    count = 1
    for i in range(1, len(text)):
        if text[i] == text[i - 1]:
            count += 1
        else:
            encoded.append((text[i - 1], count))
            count = 1
    encoded.append((text[-1], count))
    return ''.join(f"{char}{count}" if count > 1 else char for char, count in encoded)


def huffman_encode(text):
    # Apply RLE as a pre-processing step
    rle_text = run_length_encode(text)

    frequency = Counter(rle_text)
    root = build_huffman_tree(frequency)
    codes = build_huffman_codes(root)

    # Convert text to bitarray using Huffman codes
    encoded_bits = bitarray()
    encoded_bits.encode({char: bitarray(code) for char, code in codes.items()}, rle_text)

    # Serialize the Huffman tree
    serialized_tree = serialize_tree(root)
    tree_bits = bitarray()
    tree_bits.frombytes(serialized_tree.encode('utf-8'))

    # Combine tree size, serialized tree, and encoded data
    result = bitarray()
    result.frombytes(len(tree_bits).to_bytes(4, byteorder='big'))
    result.extend(tree_bits)
    result.extend(encoded_bits)

    return result.tobytes()


def huffman_decode(data):
    bits = bitarray()
    bits.frombytes(data)

    # Extract the tree size
    tree_size = int.from_bytes(bits[:32].tobytes(), byteorder='big')

    # Extract and deserialize the tree
    tree_bits = bits[32:32 + tree_size]
    tree_string = tree_bits.tobytes().decode('utf-8')
    root = deserialize_tree(tree_string)

    # Decode the data
    encoded_bits = bits[32 + tree_size:]
    decoded_text = ""
    current_node = root
    for bit in encoded_bits:
        if bit:
            current_node = current_node.right
        else:
            current_node = current_node.left

        if current_node.char is not None:
            decoded_text += current_node.char
            current_node = root

    # Reverse RLE
    final_text = ""
    i = 0
    while i < len(decoded_text):
        char = decoded_text[i]
        i += 1
        count = ""
        while i < len(decoded_text) and decoded_text[i].isdigit():
            count += decoded_text[i]
            i += 1
        final_text += char * (int(count) if count else 1)

    return final_text
