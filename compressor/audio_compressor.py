import wave
import struct
import pickle
from compressor.huffman import huffman_encode


class AudioCompressor:
    @staticmethod
    def compress(input_path, output_path, method):
        with wave.open(input_path, 'rb') as wf:
            params = wf.getparams()
            frames = wf.readframes(params.nframes)

        samples = struct.unpack(f"{params.nframes * params.nchannels}h", frames)

        if method == "lossless":
            # Use Huffman coding for lossless compression
            encoded_samples, codes = huffman_encode(samples)

            # Save encoded data and Huffman codes
            with open(output_path, 'wb') as f:
                pickle.dump((params, encoded_samples, codes), f)

        elif method == "quality":
            # Reduce bit depth (e.g., from 16-bit to 12-bit)
            compressed_samples = [s >> 4 << 4 for s in samples]
            compressed_frames = struct.pack(f"{len(compressed_samples)}h", *compressed_samples)

            with wave.open(output_path, 'wb') as wf:
                wf.setparams(params)
                wf.writeframes(compressed_frames)

        elif method == "performance":
            # Reduce bit depth further and downsample
            compressed_samples = [s >> 6 << 6 for s in samples[::2]]
            compressed_frames = struct.pack(f"{len(compressed_samples)}h", *compressed_samples)

            with wave.open(output_path, 'wb') as wf:
                wf.setparams(params._replace(framerate=params.framerate // 2,
                                             nframes=len(compressed_samples) // params.nchannels))
                wf.writeframes(compressed_frames)
