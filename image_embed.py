from PIL import Image, ImageFile
import string_serialize

def findNewValue(currentValue: int, embedValue: int, embedIndex: int) -> int:
    if currentValue < 0 or 255 < currentValue or embedValue < 0 or 255 < embedValue:
        raise AttributeError("Pixel value or embed data is outside of acceptable range.")
    
    setTo = (embedValue >> embedIndex) & 1
    return ((currentValue >> 1) << 1) + setTo

def getEmbeddedValue(value: int) -> int:
    if value < 0 or 255 < value:
        raise AttributeError("Pixel value or embed data is outside of acceptable range.")
    
    return value & 1

def bitsToInt(bits: list[int]) -> int:
    result = 0
    for i in range(len(bits)):
        result += bits[i] << i
    return result



def embed(image: ImageFile.ImageFile, data: tuple[bytearray, bytearray, bytearray]):
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
        size.append(bitsToInt(bits))
        if (i == 2):
            currentPixel += 8
    return string_serialize.bytesToUint32(size)



def extract(image: ImageFile.ImageFile) -> tuple[bytearray, bytearray, bytearray]:
    currentPixel = 0
    messageLength = getMessageSize(image)
    p = image.load()
    width = image.size[0]
    height = image.size[1]

    data = (bytearray(), bytearray(), bytearray())
    bits = []
    for i in range(messageLength + 4):
        for j in range(8):
            bits.append(getEmbeddedValue(p[(currentPixel + j) % width, (currentPixel + j) // width][i % 3]))
        data[i % 3].append(bitsToInt(bits))
        bits.clear()
        if (i % 3 == 2):
            currentPixel += 8
    return data
        
