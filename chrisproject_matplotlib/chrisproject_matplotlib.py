#
# chrisproject_matplotlib ds ChRIS plugin app
#
# (c) 2022 Fetal-Neonatal Neuroimaging & Developmental Science Center
#                   Boston Children's Hospital
#
#              http://childrenshospital.org/FNNDSC/
#                        dev@babyMRI.org
#

import os
from chrisapp.base import ChrisApp
from scipy import ndimage
import matplotlib.pyplot as plt
import nibabel as nib
import numpy as np

Gstr_title = r"""
      _          _                     _           _                     _         _       _   _ _ _     
     | |        (_)                   (_)         | |                   | |       | |     | | | (_) |    
  ___| |__  _ __ _ ___ _ __  _ __ ___  _  ___  ___| |_   _ __ ___   __ _| |_ _ __ | | ___ | |_| |_| |__  
 / __| '_ \| '__| / __| '_ \| '__/ _ \| |/ _ \/ __| __| | '_ ` _ \ / _` | __| '_ \| |/ _ \| __| | | '_ \ 
| (__| | | | |  | \__ \ |_) | | | (_) | |  __/ (__| |_  | | | | | | (_| | |_| |_) | | (_) | |_| | | |_) |
 \___|_| |_|_|  |_|___/ .__/|_|  \___/| |\___|\___|\__| |_| |_| |_|\__,_|\__| .__/|_|\___/ \__|_|_|_.__/ 
                      | |            _/ |           ______                  | |                          
                      |_|           |__/           |______|                 |_|                          
"""

Gstr_synopsis = """

(Edit this in-line help for app specifics. At a minimum, the 
flags below are supported -- in the case of DS apps, both
positional arguments <inputDir> and <outputDir>; for FS and TS apps
only <outputDir> -- and similarly for <in> <out> directories
where necessary.)

    NAME

       chrisproject_matplotlib

    SYNOPSIS

        docker run --rm fnndsc/pl-chrisproject-matplotlib chrisproject_matplotlib                     \\
            [-h] [--help]                                               \\
            [--json]                                                    \\
            [--man]                                                     \\
            [--meta]                                                    \\
            [--savejson <DIR>]                                          \\
            [-v <level>] [--verbosity <level>]                          \\
            [--version]                                                 \\
            <inputDir>                                                  \\
            <outputDir> 

    BRIEF EXAMPLE

        * Bare bones execution

            docker run --rm -u $(id -u)                             \
                -v $(pwd)/in:/incoming -v $(pwd)/out:/outgoing      \
                fnndsc/pl-chrisproject-matplotlib chrisproject_matplotlib                        \
                /incoming /outgoing

    DESCRIPTION

        `chrisproject_matplotlib` ...

    ARGS

        [-h] [--help]
        If specified, show help message and exit.
        
        [--json]
        If specified, show json representation of app and exit.
        
        [--man]
        If specified, print (this) man page and exit.

        [--meta]
        If specified, print plugin meta data and exit.
        
        [--savejson <DIR>] 
        If specified, save json representation file to DIR and exit. 
        
        [-v <level>] [--verbosity <level>]
        Verbosity level for app. Not used currently.
        
        [--version]
        If specified, print version number and exit. 
"""


class ChrisprojectMatplotlib(ChrisApp):
    """
    Create static, animated, and interactive visualizations with Matplotlib for ChRIS
    """
    PACKAGE = __package__
    TITLE = 'A ChRIS plugin app for Matplotlib'
    CATEGORY = ''
    TYPE = 'ds'
    ICON = ''  # url of an icon image
    MIN_NUMBER_OF_WORKERS = 1  # Override with the minimum number of workers as int
    MAX_NUMBER_OF_WORKERS = 1  # Override with the maximum number of workers as int
    MIN_CPU_LIMIT = 2000  # Override with millicore value as int (1000 millicores == 1 CPU core)
    MIN_MEMORY_LIMIT = 8000  # Override with memory MegaByte (MB) limit as int
    MIN_GPU_LIMIT = 0  # Override with the minimum number of GPUs as int
    MAX_GPU_LIMIT = 0  # Override with the maximum number of GPUs as int

    # Use this dictionary structure to provide key-value output descriptive information
    # that may be useful for the next downstream plugin. For example:
    #
    # {
    #   "finalOutputFile":  "final/file.out",
    #   "viewer":           "genericTextViewer",
    # }
    #
    # The above dictionary is saved when plugin is called with a ``--saveoutputmeta``
    # flag. Note also that all file paths are relative to the system specified
    # output directory.
    OUTPUT_META_DICT = {}

    def define_parameters(self):
        """
        Define the CLI arguments accepted by this plugin app.
        Use self.add_argument to specify a new app argument.
        """
        self.add_argument(
            "-x",
            "--xslices",
            dest="xslices",
            default="5",
            optional=True,
            type=int,
            help="Number of slices on the x axis",
        )
        self.add_argument(
            "-y",
            "--yslices",
            dest="yslices",
            default="5",
            optional=True,
            type=int,
            help="Number of slices on the y axis",
        )
        self.add_argument(
            "-z",
            "--zslices",
            dest="zslices",
            default="5",
            optional=True,
            type=int,
            help="Number of slices on the z axis",
        )
        self.add_argument(
            "-rx",
            "--rotatex",
            dest="rotatex",
            default="0",
            optional=True,
            type=int,
            help="Rotate how many degrees on the x axis (positive for counter-clockwise)",
        )
        self.add_argument(
            "-ry",
            "--rotatey",
            dest="rotatey",
            default="0",
            optional=True,
            type=int,
            help="Rotate how many degrees on the y axis (positive for counter-clockwise)",
        )
        self.add_argument(
            "-rz",
            "--rotatez",
            dest="rotatez",
            default="0",
            optional=True,
            type=int,
            help="Rotate how many degrees on the z axis (positive for counter-clockwise)",
        )
        self.add_argument(
            "-s",
            "--size",
            dest="size",
            default="NA",
            optional=True,
            type=str,
            help="The pixel size of image, like 640,480 for 640 * 480",
        )

    def run(self, options):
        """
        Define the code to be run by this plugin app.
        """
        print(Gstr_title)
        print('Version: %s' % self.get_version())

        for file in os.listdir(options.inputdir):
            if file.endswith(".nii"):
                data = nib.load(os.path.join(options.inputdir, file))
                if options.size == "NA":
                    fig = plt.figure()
                else:
                    _x, _y = options.size.split(',')
                    fig = plt.figure(figsize=(int(_x) / 100, int(_y) / 100))
                fig.subplots_adjust(hspace=0.4, wspace=0.4)

                x_intervals = np.linspace(1, data.shape[0], num=options.xslices + 2, dtype=int)
                y_intervals = np.linspace(1, data.shape[1], num=options.yslices + 2, dtype=int)
                z_intervals = np.linspace(1, data.shape[2], num=options.zslices + 2, dtype=int)

                print(data.shape[0], data.shape[1], data.shape[2])

                data_to_plot = data.get_fdata()

                counter = 1
                for i in range(1, options.xslices + 1):
                    ax = fig.add_subplot(3, options.xslices, i)
                    ax.set_axis_off()
                    rotated_img = ndimage.rotate(data_to_plot[x_intervals[counter] - 1, :, :], options.rotatex,
                                                 reshape=True, mode='nearest')
                    plt.imshow(rotated_img)

                    ax.set_title("%d/%d ∠%d°" % (x_intervals[counter], data.shape[0], options.rotatex))

                    counter += 1

                counter = 1
                for i in range(options.xslices + 1, options.xslices + options.yslices + 1):
                    ax = fig.add_subplot(3, options.yslices, i + options.yslices - options.xslices)
                    ax.set_axis_off()
                    rotated_img = ndimage.rotate(data_to_plot[:, y_intervals[counter] - 1, :], options.rotatey,
                                                 reshape=True, mode='nearest')
                    plt.imshow(rotated_img)

                    ax.set_title("%d/%d ∠%d°" % (y_intervals[counter], data.shape[1], options.rotatey))

                    counter += 1

                counter = 1
                for i in range(options.xslices + options.yslices + 1,
                               options.xslices + options.yslices + options.zslices + 1):
                    ax = fig.add_subplot(3, options.zslices, i + options.zslices * 2 - options.xslices - options.yslices)
                    ax.set_axis_off()
                    rotated_img = ndimage.rotate(data_to_plot[:, :, z_intervals[counter] - 1], options.rotatez,
                                                 reshape=True, mode='nearest')
                    plt.imshow(rotated_img)

                    ax.set_title("%d/%d ∠%d°" % (z_intervals[counter], data.shape[2], options.rotatez))

                    counter += 1

                fig.savefig(os.path.join(options.outputdir, os.path.splitext(file)[0] + ".png"))

    def show_man_page(self):
        """
        Print the app's man page.
        """
        print(Gstr_synopsis)
