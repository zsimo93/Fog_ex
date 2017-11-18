FROM zsimo/python-image:basex86

RUN mkdir -p /ffmpeg-static
ADD ffmpeg-static /ffmpeg-static
ENV PATH="/ffmpeg-static:${PATH}"

RUN pip install ffmpy

CMD ["/bin/bash", "-c", "cd pythonAction && python -u actionproxy.py"]
