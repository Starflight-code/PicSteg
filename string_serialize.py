def serialize(some_string: str) -> tuple[[], [], []]:
    byte_string = bytes(some_string)
    rgb_bytes = ([], [], [])
    for i in range(len(byte_string)):
        rgb_bytes[i % 3].append(byte_string[i])
    return rgb_bytes

def deserialize(rgb_bytes: tuple[[], [], []]) -> str:
    byte_string = b''
    