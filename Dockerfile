# Python version can be changed, e.g.
# FROM python:3.8
# FROM docker.io/fnndsc/conda:python3.10.2-cuda11.6.0
FROM docker.io/python:3.10.2-slim-buster

LABEL org.opencontainers.image.authors="FNNDSC <dev@babyMRI.org>" \
      org.opencontainers.image.title="DCM-2-IMG" \
      org.opencontainers.image.description="A ChRIS plugin that converts medical images (typically DICOM) to more friendly JPG/PNG format."

WORKDIR /usr/local/src/pl-dcm2img

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
RUN pip install .

CMD ["dcm2img", "--help"]
