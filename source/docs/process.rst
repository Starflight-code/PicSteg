PicSteg's Design and Data Pipelines
===================================

PicSteg is designed to embed data within images, in a way that isn't noticable to the casual observer. To do so, PicSteg embeds data into the least significant
bit of each color channel.

.. warning::
    PicSteg should not be treated as secure for important or covert communication, since it may be vulnurable to some statistical based detection methods. If you 
    expect inspection by a skilled adversary, use a program that uses more complex (and harder to detect) embedding methods, like 
    `HSI color model embedding <https://khan-muhammad.github.io/public/papers/HSI_2014.pdf>`__. 
