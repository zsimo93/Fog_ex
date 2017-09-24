FROM zsimo/python-image:base

RUN sudo apt-get update && apt-get install python-imaging

RUN mv /usr/lib/python2.7/dist-packages/PIL/_imaging.arm-linux-gnueabihf.so /usr/lib/python2.7/dist-packages/PIL/_imaging.so && \
    mv /usr/lib/python2.7/dist-packages/PIL/_imagingcms.arm-linux-gnueabihf.so /usr/lib/python2.7/dist-packages/PIL/_imagingcms.so &&\
    mv /usr/lib/python2.7/dist-packages/PIL/_webp.arm-linux-gnueabihf.so /usr/lib/python2.7/dist-packages/PIL/_webp.so && \
    mv /usr/lib/python2.7/dist-packages/PIL/_imagingmath.arm-linux-gnueabihf.so /usr/lib/python2.7/dist-packages/PIL/_imagingmath.so &&\
    mv /usr/lib/python2.7/dist-packages/PIL/_imagingft.arm-linux-gnueabihf.so /usr/lib/python2.7/dist-packages/PIL/_imagingft.so && \
    mv /usr/lib/python2.7/dist-packages/PIL/_imagingmorph.arm-linux-gnueabihf.so /usr/lib/python2.7/dist-packages/PIL/_imagingmorph.so
