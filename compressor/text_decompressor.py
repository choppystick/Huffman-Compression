from compressor.huffman import huffman_decode


class TextDecompressor:
    @staticmethod
    def decompress(compressed_data, method):
        decompressed_text = huffman_decode(compressed_data)

        if method == "lossless":
            return decompressed_text
        elif method in ["quality", "performance"]:
            print("Warning: Lossy compression methods cannot be fully reversed.")
            print("Decompressed text may not match the original.")
            return decompressed_text
