from PIL import Image

def string_to_ascii8bit(text):
    binary_text = []
    for ch in text:
        # ord returns ascii code of character (as int)
        #format with string '{0:08b}' will format int into an 8 bit binary string
        binary_text.append('{0:08b}'.format(ord(ch)))
    return binary_text

# if bin_is_even = True the value will be decremented if it wasn't even before. 
# Same happens with bin_is_even = False and the value will turn odd by being decremented
def change_pixel_value(value, bin_is_even):
    if bin_is_even and value % 2 == 1:
        value -= 1  # value turns even
    elif (not bin_is_even) and value % 2 == 0:
        value -= 1  # value turns odd
    return value

def gen_encoded_image(imrgb, encoded_pixels, width):
    for i in range(len(encoded_pixels)):
        row = int(i / width)
        col = i % width
        imrgb.putpixel((col, row), encoded_pixels[i])
    return imrgb

def encode():
    # get image path and text 
    image_path = input("Please enter the path to image: ")
    text = input("Please enter the text to be encoded: ")

    #open image and extract its size info
    image = Image.open(image_path, 'r')
    imrgb = image.convert("RGB")
    width, height = imrgb.size
    num_pixels = width * height
    encoding_places_len = int(num_pixels / 3)

    #cut text to fit into image if needed
    if len(text) > encoding_places_len:
        print("The text length is too long to be encoded in this image. The text will be cut to fit image size.")
        text = text[0:encoding_places_len]

    # get ascii code for text in 8 bit binary converted to strings
    binary_text = string_to_ascii8bit(text)

    # get all pixels of image in a list and start iter() in them
    pixels = list(imrgb.getdata())
    imageiter = iter(pixels)

    print("Encoding...\n")

    # encoding
    encoded_pixels = []
    for i in range(len(binary_text)):
        # get the next three pixels
        next3 = [list(imageiter.__next__()), list(imageiter.__next__()), list(imageiter.__next__())]
        
        for j in range(8):
            pixidx = int(j / 3)  # which pixel of next3 will be encoded this time
            rgbidx = j % 3  # which of the R,G,B values of the selected pixel with be encoded this time
            
            next3[pixidx][rgbidx] = change_pixel_value(next3[pixidx][rgbidx], binary_text[i][j] == '0')

        if i == len(binary_text) - 1: #if this was the last character of text
            next3[2][2] = change_pixel_value(next3[2][2], False)  # encode 1 at lsb of last pixel's blue value (the blue value is the last in RGB)
        else:
            next3[2][2] = change_pixel_value(next3[2][2], True)  # encode 0 at lsb of last pixel's blue value

        for j in range(3):
            encoded_pixels.append(tuple(next3[j]))

    encoded_image = gen_encoded_image(imrgb, encoded_pixels, width)

    new_img_name = input("Please enter the path for the new image: ")
    encoded_image.save(new_img_name, str(new_img_name.split(".")[1].upper()))
    print("Successfully encoded image!\n\n\n")

def decode():
    # get image path and text 
    image_path = input("Please enter the path to image: ")
    text = ""

    #open image and extract its size info
    image = Image.open(image_path, 'r')
    imrgb = image.convert("RGB")
    width, height = imrgb.size
    num_pixels = width * height
    encoding_places_len = int(num_pixels / 3)

    # get all pixels of image in a list and start iter() in them
    pixels = list(imrgb.getdata())
    imageiter = iter(pixels)

    print("Decoding...\n")

    # decoding
    text = ""
    for i in range(encoding_places_len):
        # get the next three pixels
        next3 = [list(imageiter.__next__()), list(imageiter.__next__()), list(imageiter.__next__())]
        
        binary_ascii = ''
        for j in range(8):
            pixidx = int(j / 3)  # which pixel of next3 will be encoded this time
            rgbidx = j % 3  # which of the R,G,B values of the selected pixel with be encoded this time
            
            if next3[pixidx][rgbidx] % 2 == 0:
                binary_ascii += "0"
            else:
                binary_ascii += "1"

        text += chr(int(binary_ascii, base=2))

        if next3[2][2] % 2 == 1: #text is complete
            break
    print(f"The decoded text is:\n{text}\n\n\n")


if __name__ == '__main__':
    while True:
        a = input("## Image Steganography Project ##\nWhat do you want to do?\n1. Encode\t2. Decode\t3. Exit\n")
        if a == "1":
            encode()
        elif a == "2":
            decode()
        elif a == "3":
            break
        else:
            print("Please enter one of the options 1, 2 or 3!\n\n")