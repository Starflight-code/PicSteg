# DO NOT USE AI FOR THIS, IT WILL NOT KNOW WHAT ANYTHING HERE IS

def serialize(some_string: str, pixels: int) -> tuple[bytearray(), bytearray(), bytearray()]:
    """
    Takes a string and splits it into bytestreams for each color channel, checks that data can fit in pixels provided.
    The message may be corrupted due to error resolution (replace) in UTF-8 encoding, if non-UTF-8 encodable characters are present.
   :param str some_string: a string to encode as a message
   :param int pixels: the total pixels in the target image
   :return: a bytearray for each color channel, for embedding into a target image
   :raises AttributeError: if the string length is larger than 2^32-1 (can't be fit in length header) or message is too long for image size
   :rtype: tuple[bytearray(), bytearray(), bytearray()]
    """
    byte_string = bytearray(some_string.encode(encoding="utf-8", errors="replace"))
    size = len(byte_string)
    if pow(2, 32) < size or pixels * 3 < size * 8 + 32:
        # if embedded string length can not be fit within a 32 bit uint or data can not be fit within image size
        raise AttributeError("String size is out of 32 bit unsigned integer range and/or image is too small for this message.")
    header = uint32ToBytes(size) # add size (in bytes) of encoding string (not including the size of this header) to front of bytearray
    for i in range(4):
        i = 3 - i
        byte_string.insert(0, header[i])
    
    rgb_bytes = (bytearray(), bytearray(), bytearray())
    for i in range(len(byte_string)): # breaks bit string between rgb values (to be embedded in 8 pixel blocks with a data density of 3 bits/pixel or 24 bits/pixel block)
        rgb_bytes[i % 3].append(byte_string[i])
    return rgb_bytes

def deserialize(rgb_bytes: tuple[bytearray(), bytearray(), bytearray()]) -> str:
    """
    Takes values pulled from RGB image channels and turns them back into a message string
   :param tuple[bytearray(), bytearray(), bytearray()] rgb_bytes: Bytes taken from color image channels
   :return: a string created from the UTF-8 (assumed) bytestream pulled from the image channels
   :raises UnicodeDecodeError: if the bytes provided are not valid UTF-8
   :rtype: str
    """
    byte_string = bytearray()

    for i in range(len(rgb_bytes[0]) + len(rgb_bytes[1]) + len(rgb_bytes[2])): # pulls data from pixel block data, into byte_string
        byte_string.append(rgb_bytes[i % 3][i // 3])
    
    return byte_string[4:].decode(encoding="utf-8")

    
def uint32ToBytes(number: int) -> bytearray:
    """
    Split a 32-bit unsigned integer into a bytearray of length 4
   :param int number: Some number to split up
   :return: a byte array containing the number
   :raises AttributeError: if the number is too small (negative) or too large (over 2^32 - 1)
   :rtype: bytearray
    """
    if pow(2, 32) < number or number < 0:
        raise AttributeError("Number is out of 32-bit unsigned integer range.")
    output = bytearray()
    for i in range(4): # uses bitwise operations to split 32 bit number into 4 bytes
        output.insert(0, (number >> (i * 8)) % 256)
    return output

def bytesToUint32(byte_string: bytearray) -> int:
    """
    Combine a bytearray of length 4 into a 32-bit unsigned integer
   :param bytearray byte_string: An array to combine
   :return: a number representing the array content
   :raises AttributeError: if the array length is under 4 bytes
   :rtype: bytearray
    """
    if len(byte_string) < 4:
        raise AttributeError("Byte string is under 4 bytes and can not represent a 32 bit number.")
    output = 0
    for i in range(4): # uses bitwise operations to split 32 bit number into 4 bytes
        output += byte_string[i] * pow(2, (3 - i) * 8)
    return output