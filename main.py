# DO NOT USE AI FOR THIS, IT WILL NOT KNOW WHAT ANYTHING HERE IS
import random

from PIL import Image
import string_serialize

if __name__ == '__main__':
    inputAccepted = False
    while(not inputAccepted):
        try:
            #path = input("Enter an image path: ")
            path = "8171-zucktrade.png"
            image = Image.open(path, formats=None)
            inputAccepted = True
        except:
            pass
    width, height = image.size
    p = image.load()
    print(width, height)





# Iterate over each pixel
for y in range(height):
    for x in range(width):
        # Get the pixel value
        r = random.randint(0, 100)
        g = random.randint(0, 255)
        b = random.randint(0, 120)

        new_pixel = (r, g, b)  # Red color
        image.putpixel((x, y), new_pixel)

image.save("modified.png")
"""
serialized = string_serialize.serialize("test string", 100)
print(string_serialize.deserialize(serialized))
"""