User Guide
==========

How do I hide a message?
------------------------

When you launch PicSteg, you'll be greeted by the main menu. From here you can select from a few options: message reading (r), 
message writing (w), and program exit (q).

.. code-block:: text

    Would you like to read or write to this image or exit (r/w/q)? 

To write an image, you'll want to type 'w' (without the single quotes). You'll have to provide a path to an image to hide your 
message in and provide a message. Once you provide an output path, the process is complete.

.. code-block:: text

    Would you like to read or write to this image or exit (r/w/q)? w   
    Enter an image path: my_image_path.png
    Enter a message to write: A VERY secret, hidden message. I'm hiding this one using a tool named PicSteg!!!           
    Enter an output image path: my-output-image.png

How do I retrieve a message from an altered image? 
--------------------------------------------------

It couldn't be simpler, type 'r' this time and enter a path to an image you embedded a secret message in. You'll see your message appear
in the terminal.

.. code-block:: text
    ::emphasis-lines: 4

    Would you like to read or write to this image or exit (r/w/q)? r
    Enter an image path: my_image_path.png
    --Message Start--
    A VERY secret, hidden message. I'm hiding this one using a tool named PicSteg!!! 
    --Message End--
