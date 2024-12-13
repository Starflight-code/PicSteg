from PIL import Image


def embed_serialized_data(image_path, output_path, serialized_data):
    img = Image.open(image_path)
    img = img.convert("RGB")  # Ensure the image is in RGB mode
    pixels = img.load()

    # Flatten and combine the serialized data from RGB channels
    flattened_data = []
    for channel in serialized_data:
        flattened_data.extend(channel)

    binary_data = ''.join(format(byte, '08b') for byte in flattened_data)

