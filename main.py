from PIL import Image
inputAccepted = False

while(not inputAccepted):
    try:
        #path = input("Enter an image path: ")
        path = "/home/kobiske/vscode/PicSteg/8171-zucktrade.png"
        image = Image.open(path, formats=None)
        inputAccepted = True
    except:
        pass
width, height = image.size
p = image.load()
print(width, height)