PicSteg's Design and Data Pipelines
===================================

PicSteg is designed to embed data within images, in a way that isn't noticable to the casual observer. To do so, PicSteg embeds data into the least significant
bit of each color channel. We achieve a data density of 3 bits per pixel using our grouped bit striping technique and efficient reads on large images using our
image length header. 

.. warning::
    PicSteg should not be treated as secure for important or covert communication, since it may be vulnurable to some statistical based detection methods. If you 
    expect inspection by a skilled adversary, use a program that uses more complex (and harder to detect) embedding methods, like 
    `HSI color model embedding <https://khan-muhammad.github.io/public/papers/HSI_2014.pdf>`__. 

How is data encoded for grouped bit striping?
---------------------------------------------

Let's use the following demonstration bitstream to demonstrate how data is seperated into color streams.

.. code-block:: text

    Hexadecimal / Binary / Decimal
    0x1F1E7E / 0b000111110001111001111110 / 2,039,422

Now, to turn the above 3 bytes of binary data (displayed in Hexadecimal, Binary, and Decimal for your viewing pleasure) we can use alternate between
the three colors (RGB) and produce a bytestream. Our result for the above example will come out as the below (we are alternating in RGB order).

.. code-block:: text

    Red: 0x1F / 0b00011111 / 31
    Green: 0x1E / 0b00011110 / 30
    Blue: 0x7E / 0b01111110 / 126

We've split up our colors, now what? How do we sneak this inside an image?

How do we embed our message?
----------------------------

We have our color data, let's get an example 8 image pixels with a color depth of 8 bits per pixel with three color channels. (We support PNG and JPEG, with JPEG
lacking support for an alpha channel. Since it lacks support, we won't add 4 channel embedding support for PNG only and we'll just use a single embedding process 
for all supported formats).

.. code-block:: text

    HEX / Binary (8x 8-bit values)
    R: 7E 59 40 F8 D9 28 59 38 / 01111110 01011001 01000000 11111000 11011001 00101000 01011001 00111000
    G: 49 D8 9E 8A 78 98 D8 99 / 01001001 11011000 10011110 10001010 01111000 10011000 11011000 10011001
    B: 93 58 93 25 48 23 09 58 / 10010011 01011000 10010011 00100101 01001000 00100011 00001001 01011000

With our sample data, let's add it to the above pixel data. First, let's go into how LSB (Least Significant Bit) steganography works. We each 8 bit value and look
for our least significant bit (this is the bit that affects the number's value the least when flipped or the rightmost bit) and change it to a 1 or 0 depending
on the value of our message bit. Let's start with our Red values.

.. code-block:: text

    HEX / Binary (8x 8-bit values)
    R: 7E 59 40 F8 D9 28 59 38 / 01111110 01011001 01000000 11111000 11011001 00101000 01011001 00111000
    Least Significant Bits (LSBs) in the above binary: 01001010
    Binary to Embed: 00011111
    New R: 7E 58 40 F9 D9 29 59 39 / 01111110 01011000 01000000 11111001 11011001 00101001 01011001 00111001

We can follow the same process to embed our G (green) and B (blue) values as well. We get the following result once we're done.

.. code-block:: text

    Red Message: 0x1F / 0b00011111
    Green Message: 0x1E / 0b00011110
    Blue Message: 0x7E / 0b01111110
    New R: 7E 58 40 F9 D9 29 59 39 / 01111110 01011000 01000000 11111001 11011001 00101001 01011001 00111001
    New G: 48 D8 9E 8B 79 99 D9 98 / 01001000 11011000 10011110 10001011 01111001 10011001 11011001 10011000
    New B: 92 59 93 25 49 23 09 58 / 10010010 01011001 10010011 00100101 01001001 00100011 00001001 01011000

To recover our plaintext message, we can read the LSB of each color channel of our image.

How do we know when to stop reading?
------------------------------------

Images can be quite large and our message may not take up the entire image. We know how long our message is by taking
the length of our message, during the embedding stage, and attaching it to the front of the message. Now, we can read
the first 16 pixels and get our length (stored as a 32 bit unsigned integer), so we know exactly how much of the image 
to read.