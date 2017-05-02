                        OSRA: Optical Structure Recognition Application

							Igor Filippov, 2007-2012
							igorf@helix.nih.gov


Description:

OSRA is a utility designed to convert graphical representations of
chemical structures, as they appear in journal articles, patent documents,
textbooks, trade magazines etc., into SMILES (Simplified Molecular
Input Line Entry Specification - see http://en.wikipedia.org/wiki/SMILES ) - 
a computer recognizable molecular structure format.  OSRA can read a document 
in any of the over 90 graphical formats parseable by ImageMagick - including 
GIF, JPEG, PNG, TIFF, PDF, PS etc., and generate the SMILES representation of
the molecular structure images encountered within that document.

Note that any software designed for optical recognition is unlikely to
be perfect, and the output produced might, and probably will, contain
errors, so a curation by a human knowledgeable in chemical structures 
is highly recommended.

Source code and pre-compiled binaries (compiled with MinGW suite for
Windows platform) are available from:
http://cactus.nci.nih.gov/osra
http://osra.sf.net 

Plugins:
Starting with version 1.3.7 plugins are available for download from http://osra.sourceforge.net;
Plugins for ChemBioDraw and Symyx Draw are included in Windows installer; ChemAxon MarvinSketch
supports OSRA starting with version 5.3.3.

A perl script osra-pdf  is available in package/linux/ in the source distribution and for download on osra.sourceforge.net.  
This is a script to run OSRA processing on images and PDF files with higher quality output than what is produced with the default options,
It is expected to be useful mainly for PDF files. It works by running OSRA with multiple combinations of
image processing options and automatically selecting and filtering for the best possible molecular structure. Be prepared 
that it is much slower than a regular OSRA run. You can modify the option set or the filtering criteria to better suit your needs.
OpenBabel perl binding are required to run this script.

Starting with version 1.4.0 OSRA is capable of recognizing reactions.
To run reaction recognition use the output formats rxn, rsmi, or cmlr:
osra -f rxn input.pdf -w output.rxn

=============================================================================
Dependencies:

OSRA needs the following Open Source libraries installed:

- GraphicsMagick, image manipulation library (faster ImageMagick clone)
version 1.3.7 or later. Note that versions 1.3.13 and 1.3.14 seem to have
a regression when parsing PNG files, I recommend version 1.3.12 for the time
being.
if installing from RPM make sure you have the following packages:
	GraphicsMagick
	GraphicsMagick-devel
	GraphicsMagick-c++-devel
	GraphicsMagick-c++ 
http://www.graphicsmagick.org/

- POTRACE, vector tracing library, version 1.9 or later,
http://potrace.sourceforge.net/

- GOCR/JOCR, optical character recognition library, specially patched version 0.50pre
available from http://osra.sourceforge.net is recommended.
Project website is http://jocr.sourceforge.net/

- OCRAD, optical character recognition program, version 0.21 or later. 
http://www.gnu.org/software/ocrad/ocrad.html

- TCLAP, Templatized C++ Command Line Parser Library, version 1.2.0,
http://tclap.sourceforge.net/

- OpenBabel, open source chemistry toolbox, version 2.3.0 or later; 
if installing from RPM make sure you have the following packages:
	 openbabel 
	 openbabel-devel
http://openbabel.sourceforge.net/wiki/Main_Page

=============================================================================
Other acknowledgements:

OSRA also makes use of the following software (you do not need to
install it separately, it's included in the distribution):

- ThinImage, C code from the article
  "Efficient Binary Image Thinning using Neighborhood Maps"
  by Joseph M. Cychosz, 3ksnn64@ecn.purdue.edu
  in "Graphics Gems IV", Academic Press, 1994
http://www.acm.org/pubs/tog/GraphicsGems/gemsiv/thin_image.c

- GREYCstoration, Anisotropic smoothing plugin,
http://www.greyc.ensicaen.fr/~dtschump/greycstoration/

- CImg, The C++ Template Image Processing Library,
http://cimg.sourceforge.net

- MCDL utility from Sergei Trepalin and Andrei Gakh for 2D coordinate generation

- Unpaper, is a post-processing tool for scanned sheets of paper, especially for book pages that have been scanned from previously created photocopies. The main purpose is to make scanned book pages better readable on screen after conversion to PDF. Additionally, unpaper might be useful to enhance the quality of scanned pages before performing optical character recognition (OCR). 
http://unpaper.berlios.de/

=============================================================================
Compilation:

General notes: 
Potrace (as of version 1.9) can install libpotrace.a and potracelib.h files. Run ./configure --with-libpotrace;make;make install 
or ./configure --with-libpotrace --disable-shared... for static only library.

GOCR compilation (use the patched version from OSRA website: ./configure; make libs; make install.

GraphicsMagick++-config should be in the PATH.
Depending on your installation you might also have to set up LD_LIBRARY_PATH to include /usr/local/lib.

TCLAP:
./configure; make; make install

OCRAD:
if compiling libosra later on - 
./configure CXXFLAGS=-fPIC LDFLAGS=-fPIC
otherwise - 
./configure
then -  
make; make install

libosra: You can create a library version of OSRA (libosra.a and one of the
following - libosra.so, libosra.dylib, or libosra.dll) by adding
--enable-lib command-line option to ./configure

libosra_java: set up JAVA_HOME environment variable and use --enable-java
option to configure. See addons/java/net/sf/osra/ and
addons/lib_java_sample/net/sf/osra/ on examples of usage.
If you're not getting any output try setting up LD_PRELOAD environment
variable:
LD_PRELOAD=/usr/local/lib/libopenbabel.so $JAVA_HOME/bin/java TestOsra
(taken from openbabel-2.3.0/scripts/java/README).
=========================================================================
Compiling on Linux/Unix systems:

If compiling GraphicsMagick from source check the output of configure run to make sure all of the important image formats are
getting configured (PNG, JPEG, TIFF) and that it finds GhostScript (gs).
On Linux you might want to use:
./configure --enable-shared
make
make install

Unpack OSRA package. Starting with 1.3.7 the build process is simplified to the common procedure:
./configure
make
make install

You can now optionally add Tesseract (2.0 for OSRA-1.3.7, 3.0 for OSRA-1.3.8, 3.01 for OSRA-1.3.9)  and Cuneiform OCR engines to OSRA. For Tesseract simply run configure
with:
./configure --with-tesseract 
assuming it's installed in a common location. For Cuneiform
(cuneiform-linux-1.1.0) it is now simply:
./configure --with-cuneiform 
You might have to add the path to the libraries to LD_LIBRARY_PATH.
==========================================================================
Compiling on Mac OS X:
To have static libraries install through MacPorts the following:
libxml2, libiconv, zlib, bzip2, freetype, libpng, tiff, lcms, 
jasper.

Download and compile JPEG.

OpenBabel:
export LDFLAGS=/usr/local/lib/libiconv.a
mkdir build
cd build
cmake -DBUILD_SHARED=OFF ../

GraphicsMagick (make sure GraphicsMagick++-config script is in your PATH):
./configure --disable-shared --with-x=no --disable-openmp --without-threads --prefix=/Users/igor/build LDFLAGS=-L/Users/igor/build/lib CPPFLAGS=-I/Users/igor/build/include
make
make install

OSRA (static linking):
./configure --enable-static-linking --disable-graphicsmagick-config --with-graphicsmagick-include=/Users/igor/build/include/GraphicsMagick --with-graphicsmagick-lib=/Users/igor/build/lib
make
=============================================================================
Compiling on Windows:
It is possible to compile OSRA using either Cygwin or MinGW environment,
however it appears that Cygwin-compiled executable runs about two orders of
magnitude slower than a Linux version running on an equivalent class CPU.
Therefore it is strongly recommended NOT to use Cygwin to compile OSRA.

The instructions below are for MinGW environment.
Before you compile GraphicsMagick it is necessary to install the pre-requisite
libraries - zlib, bzip2, jasper (I was able to compile only version 1.701.0
and not the later 1.900.1), jbigkit, jpeg-6b, lcms (1.19 not lcms2), libpng, tiff (3.8.2, not the later 3.9.3, 3.9.4).
You can read "ADD-ON LIBRARIES & PROGRAMS" for GraphicsMagick which
seems to apply to ImageMagick as well: http://www.graphicsmagick.org/www/README.html

Whenever "configure" script was available I used the following options:
./configure --disable-shared LDFLAGS=-L/usr/local/lib CPPFLAGS=-I/usr/local/include

To configure GraphicsMagick I used the following options:
./configure --disable-shared --without-threads --disable-openmp LDFLAGS=-L/usr/local/lib/ CPPFLAGS=-I/usr/local/include/

Compile and install GraphicsMagick, GOCR, Potrace (libpotrace.a does not get install by default), TCLAP, OCRAD.

Compiling OpenBabel version 2.3.0:
First make sure zlib, eigen2, and libxml2 are installed. For libxml2 I used the following
options for configure: --without-threads --disable-shared;

Run cmake with the following options:
cmake.exe   -G"MSYS Makefiles" -DZLIB_LIBRARY=/usr/local/lib/libz.a -DZLIB_INCLUDE_DIR=/usr/local/inclulde -DEIGEN2_INCLUDE_DIR=/usr/local/include/eigen2 -DLIBXML2_LIBRARIES=/usr/local/lib/libxml2.a -DLIBXML2_INCLUDE_DIR=/usr/local/include/libxml2 -DCMAKE_INSTALL_PREFIX=/usr/local/ -DBUILD_SHARED=OFF -DCMAKE_CXX_FLAGS=-DLIBXML_STATIC -DCMAKE_C_FLAGS=-DLIBXML_STATIC -DCMAKE_CXX_STANDARD_LIBRARIES=-lws2_32 ../
make
make install

Compiling osra:
./configure --with-openbabel-lib=/usr/local/bin --enable-static-linking
make

Make sure you take a look at osra.bat to see that the environment is set
correctly. You will still need delegates.xml from ImageMagick installation
and a separately installed Ghostscript if you'd like to process PDF and
PostScript files.

=============================================================================
Usage:

OSRA can process the following types of images:

- Computer-generated 2D structures, such as found on the PubChem website,
http://pubchem.ncbi.nlm.nih.gov/, black-and-white and color (use a
resolution of 72 dpi),

- Black-and-white PDF and PostScript files, including multi-page ones. Please
note that you need Ghostcript installed for ImageMagick to be able to
parse these kinds of files. 

- Scanned images - black-and-white, a resolution of 300 dpi is recommended,
though 150 dpi can also produce fair results. Please make sure the
scanned image is of reasonable quality - an input that's too noisy will 
only generate garbage output.

Some common abbreviations, hetero atoms, fused and merged atomic
labels, hash and wedge bonds, and bridge bonds are currently
recognized. Isotopes and some element
symbols, i.e. iodine ("I" -- looks too much like a straight line = single
bond), are not.


Command-line options: 
./osra --help 
will give you a list of available options with short descriptions.

Most common use: ./osra [-r <resolution>] <filename>

Resolution in dpi, default is "0" for automatic resolution
determination.
Filename is the name of your image file (or PS/PDF document).

Other options: 
-t, --threshold: Gray level threshold, default is 0.2
                 for black-and-white images, 

-n, --negate:    Inverts colors (for white on black images),

-o, --output:    Sets a prefix for writing recognized images to files - i.e.
                 "-o tmp" will create files tmp0.png, tmp1.png... for
                 each of the structures,

-s, --size:      Resize images on output - can be useful for running OSRA
                 as a backend for a webservice. Example: "-s 300x400".

-g,  --guess:    Prints out resolution guess when you chose to have automatic
     		 resolution estimate

-p,  --print:    Prints out the value of confidence function estimate


-f,  --format:  Output format (either smi for SMILES or sdf for SD file format)

-d,  --debug:    Print out debug information on spelling corrections

-a <configfile>,  --superatom <configfile>:  Superatom label map to SMILES (superatom.txt by default)

-l <configfile>,  --spelling <configfile>:   Spelling correction dictionary (spelling.txt by default)

-u <rounds>,  --unpaper <rounds>
     Pre-process image with unpaper algorithm, rounds (default: do not pre-process)

-w <filename>, --write <filename> Write output to a file instead of stdout

-b, --bond: Print out average bond length in pixels

-j, --jaggy: Additional thinning/scaling down of low quality documents

-i, --adaptive:    Adaptive thresholding pre-processing, useful for low light/low
     contrast images

-c,  --coordinates: Show surrounding box coordinates (only for SDF/SMI/CAN output format)

--embedded-format <format>: Allows the user to have InChI or SMILES  included in an SDF file
as a molecular property

============================================================================
LICENSE:

This program is free software; the part of the software that was written 
at the National Cancer Institute is in the public domain.  This does not
preclude, however, that components such as specific libraries used in the
software may be covered by specific licenses, including but not limited
to the GNU General Public License as published by the Free Software Foundation; 
either version 2 of the License, or (at your option) any later version; 
which may impose specific terms for redistribution or modification.

This program is distributed in the hope that it will be useful, but
WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307,
USA. See also http://www.gnu.org/.

See the file COPYING for details.
====================================================================
