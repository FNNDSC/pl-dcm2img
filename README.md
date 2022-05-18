# pl-dcm2img

[![Version](https://img.shields.io/docker/v/fnndsc/pl-dcm2img?sort=semver)](https://hub.docker.com/r/fnndsc/pl-dcm2img)
[![MIT License](https://img.shields.io/github/license/fnndsc/pl-dcm2img)](https://github.com/FNNDSC/pl-dcm2img/blob/main/LICENSE)
[![ci](https://github.com/FNNDSC/pl-dcm2img/actions/workflows/ci.yml/badge.svg)](https://github.com/FNNDSC/pl-dcm2img/actions/workflows/ci.yml)

`pl-dcm2img` is a [_ChRIS_](https://chrisproject.org/)
_ds_ plugin which searches for medical image files (typically DICOM or NIfTI) in its input dir (tree) and converts these files to more image friendly formats like `png` or `jpg` in its output (tree).

## Abstract

`pl-dcm2img` is a ChRIS DS plugin wrapped around a `med2image` [module](https://github.com/FNNDSC/med2image). The plugin will search for any files in its input tree space (over all directories and subdirectories within its `inputdir`) that conform to a simple substring filter (usually a file extension such as `dcm` or `nii`) and convert these to `jpg` or `png` format.

## Installation

`pl-dcm2img` is a _[ChRIS](https://chrisproject.org/) plugin_, meaning it can
run from either within _ChRIS_ or the command-line. The recommended usage is to install and run the containerized version of the program.

[![Get it from chrisstore.co](https://ipfs.babymri.org/ipfs/QmaQM9dUAYFjLVn3PpNTrpbKVavvSTxNLE5BocRCW1UoXG/light.png)](https://chrisstore.co/plugin/pl-dcm2img)

## Local Usage

To get started with local command-line usage, use [Apptainer](https://apptainer.org/)
(a.k.a. Singularity) to run `pl-dcm2img` as a container with input data in the directory `input` and directory `output` for results:

```shell
# See below for argument meaning
singularity exec docker://fnndsc/pl-dcm2img dcm2img                     \
                --reslice --verbosity 1 --rot 100 --inputFileSubStr dcm \
                input/ output/
```

For quick help,

```shell
singularity exec docker://fnndsc/pl-dcm2img dcm2img --help
```

## Examples

As true for all ChRIS DS plugins, `dcm2img` requires two positional arguments: a directory containing input data, and a directory in which to create output data. First, create the input directory and move input data into it. For example a set of DICOM images from an FNNDSC anonymous repo

```shell
mkdir incoming/ outgoing/
cd incoming
git clone https://github.com/FNNDSC/SAG-anon
```

Now, convert all these DICOMs to PNG, keeping the directory structure in the output

```shell
singularity exec docker://fnndsc/pl-dcm2img:latest dcm2img                  \
                --reslice --verbosity 1 --rot 100 --inputFileSubStr dcm \
                incoming/ outgoing/
```

which will `reslice` the input, i.e. create images for each of the `x`, `y`, and `z` directions of the original 3D volume data, and apply a 90 degree rotation to the `x` direction images while leaving the `y` and `z` as per the original data. Note that the `inputFileSubStr` searches for files in directories in the `incoming/` directory that contain the string `dcm` anywhere in their filenames.

The complete argument list is:

```html
        [-i|--inputFile <inputFile>]
        Input file to convert. Typically a DICOM file or a nifti volume.

        [--inputFileSubStr <substr>]
        As a convenience, the input file can be determined via a substring
        search of all the files in the <inputDir> using this flag. The first
        filename hit that contains the <substr> will be assigned the
        <inputFile>.

        This flag is useful if input names are long and cumbersome, but
        a short substring search would identify the file. For example, an
        input file of

           0043-1.3.12.2.1107.5.2.19.45152.2013030808110149471485951.dcm

        can be specified using ``--inputFileSubStr 0043-``

        -o|--outputFileStem <outputFileStem>
        The output file stem to store conversion. If this is specified
        with an extension, this extension will be used to specify the
        output file type.

        SPECIAL CASES:
        For DICOM data, the <outputFileStem> can be set to the value of
        an internal DICOM tag. The tag is specified by preceding the tag
        name with a percent character '%%', so

            -o %%ProtocolName

        will use the DICOM 'ProtocolName' to name the output file. Note
        that special characters (like spaces) in the DICOM value are
        replaced by underscores '_'.

        Multiple tags can be specified, for example

            -o %%PatientName%%PatientID%%ProtocolName

        and the output filename will have each DICOM tag string as
        specified in order, connected with dashes.

        [--convertOnlySingleDICOM]
        If specified, will only convert the single DICOM specified by the
        '--inputFile' flag. This is useful for the case when an input
        directory has many DICOMS but you specifially only want to convert
        the named file. By default the script assumes that multiple DICOMS
        should be converted en mass otherwise.

        [--preserveDICOMinputName]
        If specified, use the input DICOM name as the stem of the output
        filename, with the specified type ('jpg' or 'png') as the extension.
        In the case where [--reslice] is additionally specified, only the
        slice or 'z' direction will preserve original DICOM names.

        [-t|--outputFileType <outputFileType>]
        The output file type. If different to <outputFileStem> extension,
        will override extension in favour of <outputFileType>.

        [-s|--sliceToConvert <sliceToConvert>]
        In the case of volume files, the slice (z) index to convert. Ignored
        for 2D input data. If a '-1' is sent, then convert *all* the slices.
        If an 'm' is specified, only convert the middle slice in an input
        volume.

        [-f|--frameToConvert <sliceToConvert>]
        In the case of 4D volume files, the volume (V) containing the
        slice (z) index to convert. Ignored for 3D input data. If a '-1' is
        sent, then convert *all* the frames. If an 'm' is specified, only
        convert the middle frame in the 4D input stack.

        [--showSlices]
        If specified, render/show image slices as they are created.

        [--rot <3DbinVector>]
        A per dimension binary rotation vector. Useful to rotate individual
        dimensions by an angle specified with [--rotAngle <angle>]. Default
        is '110', i.e. rotate 'x' and 'y' but not 'z'. Note that for a
        non-reslice selection, only the 'z' (or third) element of the vector
        is used.

        [--rotAngle <angle>]
        Default 90 -- the rotation angle to apply to a given dimension of the
        <3DbinVector>

        [--func <functionName>]
        Apply the specified transformation function before saving. Currently
        support functions:

            * invertIntensities
              Inverts the contrast intensity of the source image.

        [--reslice]
        For 3D data only. Assuming [x,y,z] coordinates, the default is to save
        along the 'z' direction. By passing a --reslice image data in the 'x'
        and 'y' directions are also saved. Furthermore, the <outputDir> is
        subdivided into 'slice' (z), 'row' (x), and 'col' (y) subdirectories.

        [-x|--man]
        Show full help.

        [-y|--synopsis]
        Show brief help.

        [--verbosity <level=1>]
        Control how chatty med2image is. Set to '0' for blissful silence, '1'
        for sane progress and '3' for full information.
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

(Note if you want to run `pudb` debugging, you should run the container as `root`, i.e. do not pass a `-u` CLI)

_-30-_