from PIL import Image, ImageFile
import string_serialize

def findNewValue(currentValue: int, embedValue: int, embedIndex: int) -> int:
    """
    Takes the bit at the index provided in the embedValue integer and sets the LSB of currentValue to it, 
    returns this value
   :param int currentValue: a pixel value from an image
   :param int embedValue: a byte being embedded into an image
   :param int embedIndex: the index of the pixel within its pixelCluster
   :return: an updated pixel value, with data embedded
   :raises AttibuteError: if the currentValue or embedValue are not between 0 and 255
   :raises AttibuteError: if the embedIndex is not between 0 and 7
   :rtype: int
    """
    if currentValue < 0 or 255 < currentValue or embedValue < 0 or 255 < embedValue:
        raise AttributeError("Pixel value or embed data is outside of acceptable range.")
    if embedIndex < 0 or 7 < embedIndex:
        raise AttributeError("embedIndex must index a bit in a byte (out of range: 0 to 7).")
    
    setTo = (embedValue >> embedIndex) & 1
    return ((currentValue >> 1) << 1) + setTo

def getEmbeddedValue(value: int) -> int:
    """
    Returns the least significant bit of the value provided
   :param int value: an integer between 0 and 255
   :return: a 1 or a 0 (the LSB)
   :raises AttributeError: if value is not between 0 and 255
   :rtype: int
    """

    if value < 0 or 255 < value:
        raise AttributeError("Pixel value or embed data is outside of acceptable range.")
    
    return value & 1

def bitsToByte(bits: list[int]) -> int:
    """
    Turns a list of 1s and 0s into a byte of data
   :param tuple[bytearray(), bytearray(), bytearray()] bits: a list of 1s and 0s (length of 8)
   :return: an integer between 0 and 255
   :raises AttributeError: if the list's length is less than 8
   :rtype: int
    """
    if len(bits) < 8:
        raise AttributeError("A list of length 8 is required to make a byte")

    result = 0
    for i in range(8):
        result += (bits[i] & 1) << i
    return result



def embed(image: ImageFile.ImageFile, data: tuple[bytearray, bytearray, bytearray]):
    """
    Takes an image and three bytestreams, embeds the bytestreams into the image
   :param ImageFile.ImageFile image: an image to embed the data into
   :param tuple[bytearray(), bytearray(), bytearray()] bits: three bytestreams to embed into the Red, Green, and Blue color channels respectively
   :return: None
   :rtype: None
    """
    currentPixel = 0
    width = image.size[0]
    height = image.size[1]
    p = image.load()
    pixelCluster = []
    for i in range(8): # initialize pixel cluster (8 pixel values per cluster)
        pixelCluster.append([0, 0, 0])

    for i in range(len(data[0]) + len(data[1]) + len(data[2])):
        for j in range(8): # find new values, add to pre-application cluster
            pixelCluster[j][i % 3] = findNewValue(p[(currentPixel + j) % width, (currentPixel + j) // width][i % 3], data[i % 3][i // 3], j)
        if (i % 3 == 2):
            for j in range(8): # apply cluster values
                if len(p[(currentPixel + j) % width, (currentPixel + j) // width]) == 3:
                    p[(currentPixel + j) % width, (currentPixel + j) // width] = (pixelCluster[j][0], pixelCluster[j][1], pixelCluster[j][2])
                else:
                    p[(currentPixel + j) % width, (currentPixel + j) // width] = (pixelCluster[j][0], pixelCluster[j][1], pixelCluster[j][2], p[(currentPixel + j) % width, (currentPixel + j) // width][3])
            currentPixel += 8

    for i in range(len(data[0]) + len(data[1]) + len(data[2]) % 3):
        for j in range(8): # apply cluster values
            if len(p[(currentPixel + j) % width, (currentPixel + j) // width]) == 3:
                p[(currentPixel + j) % width, (currentPixel + j) // width] = (pixelCluster[j][0], pixelCluster[j][1], pixelCluster[j][2])
            else:
                p[(currentPixel + j) % width, (currentPixel + j) // width] = (pixelCluster[j][0], pixelCluster[j][1], pixelCluster[j][2], p[(currentPixel + j) % width, (currentPixel + j) // width][3])


def getMessageSize(image: ImageFile.ImageFile) -> int:
    """
    Reads the message header within the image to determine the message size, returns it
   :param ImageFile.ImageFile image: an image containing an embedded message
   :return: a message size between 0 and 2^32 - 1
   :rtype: int
    """
    size = bytearray()
    BYTES_IN_SIZE_HEADER = 4
    width = image.size[0]
    height = image.size[1]
    p = image.load()
    currentPixel = 0

    for i in range(BYTES_IN_SIZE_HEADER):
        bits = []
        for j in range(8):
            bits.append(getEmbeddedValue(p[(currentPixel + j) % width, (currentPixel + j) // width][i % 3]))
        size.append(bitsToByte(bits))
        if (i == 2):
            currentPixel += 8
    return string_serialize.bytesToUint32(size)



def extract(image: ImageFile.ImageFile) -> tuple[bytearray, bytearray, bytearray]:
    """
    Reads the embedded message from an image file, returns the bytestreams within the image
   :param ImageFile.ImageFile image: a list of 1s and 0s (length of 8)
   :return: the bytestreams found within the color channels of the image
   :raises AttributeError: if the header contains a size above the image's capacity
   :rtype: tuple[bytearray, bytearray, bytearray]
    """
    currentPixel = 0
    messageLength = getMessageSize(image)
    p = image.load()
    width = image.size[0]
    height = image.size[1]

    if width * height * 3 < (messageLength + 4) * 8 + 32:
        # if embedded string length can not be fit within a 32 bit uint or data can not be fit within image size
        raise AttributeError("Image is too small for the message size (header corrupted?).")

    data = (bytearray(), bytearray(), bytearray())
    bits = []
    for i in range(messageLength + 4):
        for j in range(8):
            bits.append(getEmbeddedValue(p[(currentPixel + j) % width, (currentPixel + j) // width][i % 3]))
        data[i % 3].append(bitsToByte(bits))
        bits.clear()
        if (i % 3 == 2):
            currentPixel += 8
    return data
        
