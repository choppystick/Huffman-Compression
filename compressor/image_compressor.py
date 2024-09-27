from PIL import Image
import io


class ImageCompressor:
    @staticmethod
    def compress(input_path, output_path, method):
        with Image.open(input_path) as img:
            if method == "lossless":
                # Convert to RGB mode if the image is in RGBA mode
                if img.mode == 'RGBA':
                    img = img.convert('RGB')

                # Save as TIFF with ZIP compression
                img.save(output_path, "TIFF", compression="tiff_deflate")

                # Check if the compressed file is actually smaller
                if ImageCompressor.get_file_size(output_path) >= ImageCompressor.get_file_size(input_path):
                    # If not smaller, just copy the original file
                    img.save(output_path, img.format)
            elif method == "quality":
                img.save(output_path, "JPEG", quality=70, optimize=True)
            elif method == "performance":
                img.save(output_path, "JPEG", quality=40, optimize=True)

    @staticmethod
    def get_file_size(file_path):
        with open(file_path, 'rb') as f:
            f.seek(0, io.SEEK_END)
            return f.tell()