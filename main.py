# DO NOT USE AI FOR THIS, IT WILL NOT KNOW WHAT ANYTHING HERE IS

from PIL import Image
import string_serialize
import image_embed

if __name__ == '__main__':

    while(True):
        match(input("Would you like to read or write to this image or exit (r/w/q)? ").lower().strip()[0]):
            case 'r':
                while(True):
                    try:
                        path = input("Enter an image path: ")
                        image = Image.open(path, formats=None)
                        break
                    except:
                        print("That path didn't work. Try again?")
                print(f"--Message Start--\n{string_serialize.deserialize(image_embed.extract(image))}\n--Message End--")
            case 'w':
                while(True):
                    try:
                        path = input("Enter an image path: ")
                        image = Image.open(path, formats=None)
                        break
                    except:
                        print("That path didn't work. Try again?")
                message = input("Enter a message to write: ")
                width, height = image.size
                embed_arrays = string_serialize.serialize(message, width * height)
                image = image_embed.embed(image, embed_arrays)

                while(True):
                    try:
                        path = input("Enter an output image path: ")
                        image.save(path)
                        break
                    except:
                        print("That path didn't work. Try again?")
            case 'q':
                print("Goodbye!")
                exit(0)
    
