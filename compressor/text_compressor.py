from .huffman import huffman_encode
import re


class TextCompressor:
    @staticmethod
    def compress(text, method):
        if method == "lossless":
            return huffman_encode(text)
        elif method == "quality":
            # Remove punctuation and whitespace
            compressed_text = re.sub(r'[^\w\s]', '', text)
            compressed_text = ''.join(compressed_text.split())
            return huffman_encode(compressed_text)
        elif method == "performance":
            # Remove one letter from the middle of each word
            words = text.split()
            compressed_words = []
            for word in words:
                if len(word) > 1:
                    mid = len(word) // 2
                    compressed_word = word[:mid] + word[mid + 1:]
                else:
                    compressed_word = word
                compressed_words.append(compressed_word)
            compressed_text = ''.join(compressed_words)
            # Remove punctuation and whitespace
            compressed_text = re.sub(r'[^\w\s]', '', compressed_text)
            compressed_text = ''.join(compressed_text.split())

            return huffman_encode(compressed_text)
