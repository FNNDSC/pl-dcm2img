# pl-dcm2img

[![Version](https://img.shields.io/docker/v/fnndsc/pl-dcm2img?sort=semver)](https://hub.docker.com/r/fnndsc/pl-dcm2img)
[![MIT License](https://img.shields.io/github/license/fnndsc/pl-dcm2img)](https://github.com/FNNDSC/pl-dcm2img/blob/main/LICENSE)
[![ci](https://github.com/FNNDSC/pl-dcm2img/actions/workflows/ci.yml/badge.svg)](https://github.com/FNNDSC/pl-dcm2img/actions/workflows/ci.yml)

`pl-dcm2img` is a [_ChRIS_](https://chrisproject.org/)
_ds_ plugin which searches for medical image files (typically DICOM or NIfTI) in its input dir (tree) and converts these files to more image friendly formats like `png` or `jpg` in its output (tree).

## Abstract

`pl-dcm2img` is a ChRIS DS plugin around a `med2image` [module](https://github.com/FNNDSC/med2image). The plugin will search for any files in its input tree space (do all directories and subdirectories within its `inputdir`) that conform to a simple substring filter (usually a file extension such as `dcm` or `nii`) and convert these to `jpg` or `png` format.

## Installation

`pl-dcm2img` is a _[ChRIS](https://chrisproject.org/) plugin_, meaning it can
run from either within _ChRIS_ or the command-line. The recommended usage is to install and run the containerized version of the program.

[![Get it from chrisstore.co](https://ipfs.babymri.org/ipfs/QmaQM9dUAYFjLVn3PpNTrpbKVavvSTxNLE5BocRCW1UoXG/light.png)](https://chrisstore.co/plugin/pl-dcm2img)

## Local Usage

To get started with local command-line usage, use [Apptainer](https://apptainer.org/)
(a.k.a. Singularity) to run `pl-dcm2img` as a container:

```shell
singularity exec docker://fnndsc/pl-dcm2img dcm2img [--args values...] input/ output/
```

To print its available options, run:

```shell
singularity exec docker://fnndsc/pl-dcm2img dcm2img --help
```

## Examples

`dcm2img` requires two positional arguments: a directory containing
input data, and a directory where to create output data.
First, create the input directory and move input data into it.

```shell
mkdir incoming/ outgoing/
mv some.dat other.dat incoming/
singularity exec docker://fnndsc/pl-dcm2img:latest dcm2img [--args] incoming/ outgoing/
```

## Development

Instructions for developers.

### Building

Build a local container image:

```shell
docker build -t localhost/fnndsc/pl-dcm2img .
```

### Get JSON Representation

Run [`chris_plugin_info`](https://github.com/FNNDSC/chris_plugin#usage)
to produce a JSON description of this plugin, which can be uploaded to a _ChRIS Store_.

```shell
docker run --rm localhost/fnndsc/pl-dcm2img chris_plugin_info > chris_plugin_info.json
```

### Local Test Run

Mount the source code `dcm2img.py` into a container to test changes without rebuild.

```shell
docker run --rm -it --userns=host -u $(id -u):$(id -g) \
    -v $PWD/dcm2img.py:/usr/local/lib/python3.10/site-packages/dcm2img.py:ro \
    -v $PWD/in:/incoming:ro -v $PWD/out:/outgoing:rw -w /outgoing \
    localhost/fnndsc/pl-dcm2img dcm2img /incoming /outgoing
```
