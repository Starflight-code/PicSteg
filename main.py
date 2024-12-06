from PIL import Image
import string_serialize
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

"""
serialized = string_serialize.serialize("test string", 100)
print(string_serialize.deserialize(serialized))
"""