def serialize(some_string: str, pixels: int) -> tuple[bytearray(), bytearray(), bytearray()]:
    byte_string = bytearray(some_string.encode(encoding="utf-8", errors="replace"))
    size = len(byte_string)
    if pow(2, 32) < size or pixels * 3 < size * 8 + 32:
        # if embedded string length can not be fit within a 32 bit uint or data can not be fit within image size
        return None
    header = uint32ToBytes(size) # add size (in bytes) of encoding string (not including size) to front of bytearray
    for i in range(4):
        i = 3 - i
        byte_string.insert(0, header[i])
    
    rgb_bytes = (bytearray(), bytearray(), bytearray())
    for i in range(len(byte_string)):
        rgb_bytes[i % 3].append(byte_string[i])
    return rgb_bytes

def deserialize(rgb_bytes: tuple[bytearray(), bytearray(), bytearray()]) -> str:
    byte_string = bytearray()

    for i in range(len(rgb_bytes[0]) + len(rgb_bytes[1]) + len(rgb_bytes[2])):
        byte_string.append(rgb_bytes[i % 3][i // 3])
    
    return byte_string[4:].decode(encoding="utf-8")

    
def uint32ToBytes(number: int) -> bytearray:
    if pow(2, 32) < number or number < 0:
        raise AttributeError("Number is out of 32 bit unsigned integer range.")
    output = bytearray()
    for i in range(32):
        output.insert(0, (number >> i) % 256)
    return output