import struct
from PIL import Image
import numpy as np

# Convert bytes to a list of bits
def _to_bits(data_bytes: bytes):
    bit_list = []
    for single_byte in data_bytes:
        for bit_position in range(7, -1, -1):
            bit_list.append((single_byte >> bit_position) & 1)
    return bit_list


# Convert a list of bits back to bytes
def _from_bits(bit_list):
    byte_result = []
    for bit_index in range(0, len(bit_list), 8):
        current_byte = 0
        for bit_offset in range(8):
            if bit_index + bit_offset < len(bit_list):
                current_byte = (current_byte << 1) | bit_list[bit_index + bit_offset]
        byte_result.append(current_byte)
    return bytes(byte_result)


# Embed a secret message into an image using LSB steganography
def embed_message(image_input, message_data, output_path=None, level="Public"):

    image_object = image_input if isinstance(image_input, Image.Image) else Image.open(image_input).convert("RGB")

    if isinstance(message_data, str):
        message_data = message_data.encode()

    level_map = {"Public": 0, "Restricted": 1, "Confidential": 2}
    level_value = level_map.get(level, 0)

    payload_bytes = bytes([level_value]) + struct.pack(">I", len(message_data)) + message_data
    payload_bits = _to_bits(payload_bytes)

    image_array = np.array(image_object)
    height, width = image_array.shape[0], image_array.shape[1]

    if len(payload_bits) > height * width * 3:
        raise ValueError("image cannot store the message.")

    bit_pointer = 0

    for row_index in range(height):
        for column_index in range(width):
            for color_channel in range(3):
                if bit_pointer < len(payload_bits):
                    image_array[row_index, column_index, color_channel] = (
                        image_array[row_index, column_index, color_channel] & 0xFE) | payload_bits[bit_pointer]
                    bit_pointer += 1

    output_image = Image.fromarray(image_array)

    if output_path:
        output_image.save(output_path)
        return None

    return output_image


# Extract a hidden message from an image
def extract_message(image_input):

    image_object = image_input if isinstance(image_input, Image.Image) else Image.open(image_input).convert("RGB")

    image_array = np.array(image_object)
    extracted_bits = []

    for row_pixels in image_array:
        for pixel in row_pixels:
            for channel_value in pixel:
                extracted_bits.append(channel_value & 1)

    level_int = _from_bits(extracted_bits[:8])[0]
    level_map = {0: "Public", 1: "Restricted", 2: "Confidential"}
    level = level_map.get(level_int, "Public")

    message_length = struct.unpack(">I", _from_bits(extracted_bits[8:40]))[0]

    message_bytes = _from_bits(extracted_bits[40:40 + message_length * 8])

    return level, message_bytes