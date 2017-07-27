FROM zsimo/python-image:base

RUN mkdir buildPIL && cd buildPIL
COPY jpegsrc.v8c.tar.gz ./
RUN tar xvfz jpegsrc.v8c.tar.gz \
    && cd jpeg-8c \
    && ./configure --enable-shared --prefix=$CONFIGURE_PREFIX \
    && make \
    && sudo make install

RUN ln -s /usr/lib/arm-linux-gnueabi/libjpeg.so /usr/lib \
    && ln -s /usr/lib/arm-linux-gnueabi/libfreetype.so /usr/lib \
    && sudo ln -s /usr/lib/arm-linux-gnueabi/libz.so /usr/lib

RUN apt-get update \
    && apt-get install libtiff5-dev libjpeg-dev zlib1g-dev libfreetype6-dev liblcms2-dev libwebp-dev tcl8.5-dev tk8.5-dev python-tk

RUN sudo pip install Pillow
