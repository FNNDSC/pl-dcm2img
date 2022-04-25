#!/usr/bin/env python

import sys
from    pathlib             import Path
from    argparse            import ArgumentParser, Namespace, ArgumentDefaultsHelpFormatter
from    importlib.metadata  import Distribution

from    chris_plugin        import chris_plugin, PathMapper

from    med2image           import med2image
import  pudb

import  os

__pkg = Distribution.from_name(__package__)
__version__ = __pkg.version


DISPLAY_TITLE = r"""
       _           _                 _____ _
      | |         | |               / __  (_)
 _ __ | |______ __| | ___ _ __ ___  `' / /'_ _ __ ___   __ _
| '_ \| |______/ _` |/ __| '_ ` _ \   / / | | '_ ` _ \ / _` |
| |_) | |     | (_| | (__| | | | | |./ /__| | | | | | | (_| |
| .__/|_|      \__,_|\___|_| |_| |_|\_____/_|_| |_| |_|\__, |
| |                                                     __/ |
|_|                                                    |___/
"""


parser = ArgumentParser(description='''
A ChRIS plugin that converts medical images (typically DICOM) to more
friendly JPG/PNG format. This plugin is closely related to ``pl-med2img``
and supports all the same arguments; however here the code uses a more
intelligent mapper/filter to allow for trivial in-plugin parallelization.
For more information, see https://github.com/FNNDSC/pl-dcm2img
''', formatter_class=ArgumentDefaultsHelpFormatter)

parser.add_argument('-V', '--version',
                    action      = 'version',
                    version     = f'$(prog)s {__version__}'
                )
parser.add_argument('-i', '--inputFile',
                    dest        = 'inputFile',
                    help        = 'name of the input file within the inputDir',
                    default     = ''
                )
parser.add_argument("--inputFileSubStr",
                    help        = "input file substring to tag a file in the inputDir",
                    dest        = 'inputFileSubStr',
                    default     = ''
                )
parser.add_argument('-o', '--outputFileStem',
                    dest        = 'outputFileStem',
                    help        = 'output file stem name (with optional extension)',
                    default     = 'sample'
                )
parser.add_argument('-t', '--outputFileType',
                    dest        = 'outputFileType',
                    default     = '',
                    help        = 'output image file format'
                )
parser.add_argument('-s', '--sliceToConvert',
                    dest        = 'sliceToConvert',
                    default     = "-1",
                    help        = 'slice to convert (for 3D data)'
                )
parser.add_argument('-f', '--frameToConvert',
                    dest        = 'frameToConvert',
                    default     = "-1",
                    help        = 'frame to convert (for 4D data)'
                )
parser.add_argument('--printElapsedTime',
                    dest        = 'printElapsedTime',
                    action      = 'store_true',
                    default     = False,
                    help        = 'print program run time'
                )
parser.add_argument('-r', '--reslice',
                    dest        = 'reslice',
                    action      = 'store_true',
                    default     = False,
                    help        = 'save images along x, y, z directions -- 3D input only'
                )
parser.add_argument('--showSlices',
                    dest        = 'showSlices',
                    action      = 'store_true',
                    default     = False,
                    help        = 'show slices that are converted'
                )
parser.add_argument('--func',
                    dest        = 'func',
                    default     = '',
                    help        = 'apply the specified transformation function before saving'
                )
parser.add_argument('-y', '--synopsis',
                    dest        = 'synopsis',
                    action      = 'store_true',
                    default     = False,
                    help        = 'short synopsis'
                )
parser.add_argument("--convertOnlySingleDICOM",
                    help        = "if specified, only convert the specific input DICOM",
                    dest        = 'convertOnlySingleDICOM',
                    action      = 'store_true',
                    default     = False
)
parser.add_argument("--verbosity",
                    help        = "verbosity level",
                    default     = '1',
                    dest        = 'verbosity'
                )
parser.add_argument("--glob",
                    help        = "glob expression",
                    default     = '**/',
                    dest        = 'glob'
                )
parser.add_argument('--rot',
                    help    = "3D slice/dimenstion rotation vector",
                    dest    = 'rot',
                    default = "110"
                )
parser.add_argument('--rotAngle',
                    help    = "3D slice/dimenstion rotation angle",
                    dest    = 'rotAngle',
                    default = "90"
                )

# documentation: https://fnndsc.github.io/chris_plugin/chris_plugin.html#chris_plugin
@chris_plugin(
    parser              = parser,
    title               = 'pl-dcm2img',
    category            = 'Image conversion',       # ref. https://chrisstore.co/plugins
    min_memory_limit    = '100Mi',                  # supported units: Mi, Gi
    min_cpu_limit       = '1000m',                  # millicores, e.g. "1000m" = 1 CPU core
    min_gpu_limit       = 0                         # set min_gpu_limit=1 to enable GPU
)
def main(options: Namespace, inputdir: Path, outputdir: Path):
    print(DISPLAY_TITLE, file=sys.stderr)

    print('Version: %s' %  f'{__version__}')
    for k,v in options.__dict__.items():
        print("%25s:  [%s]" % (k, v))
    print("")

    pudb.set_trace()

    mapper      = PathMapper(inputdir, outputdir, glob='*/**/', only_files = False)

    for input, output in mapper:
        os.chdir('/' + inputdir.name)
        options.inputDir    = '/' + inputdir.name   + '/' + input.name
        options.outputDir   = '/' + outputdir.name  + '/' + output.name
        imgConverter        = med2image.object_factoryCreate(options).C_convert
        if imgConverter:
            imgConverter.tic()
            imgConverter.run()
            if options.printElapsedTime:
                print("Elapsed time = %f seconds" % imgConverter.toc())

if __name__ == '__main__':
    main()

