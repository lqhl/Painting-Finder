# PaintingFinder

The PaintingFinder is my graduation project of Shanghai Jiao Tong University. It can search similar pictures of a sketch in database. You can considered it as an implementation of [MindFinder: Finding Images by Sketching](http://research.microsoft.com/en-us/projects/mindfinder/). You may refer to <cite>[Cao's paper][1]</cite> for implementation details.

## How to install?

I used Python 2.7 to implement the project, and I've tested it on Ubuntu 12.04 and Windows 7. To run it, the following libraries are needed: NumPy, SciPy, matplotlib, Python Image Library, Cython (optional).

### Preprocessing

I use Benchmark and Boundary Detection Code on [The Berkeley Segmentation Dataset and Benchmark](http://www.eecs.berkeley.edu/Research/Projects/CS/vision/grouping/segbench/) to get sketches of pictures in the data set. To be continued... You can use my data set first.

### Build Index

To build binary file (ignore it if you don't have Cython):

    cd src
    make

To build the index of proprocessed pictures in folder `/data`:

    cd src
    python build_index.py

It may take several minutes.

### Run the Painter

To draw sketch and find similar pictures:

    cd src
    python painter.py


[1]: http://research.microsoft.com/apps/pubs/?id=149199 "Yang Cao, Changhu Wang, Liqing Zhang, and Lei Zhang, Edgel Inverted Index for Large-Scale Sketch-based Image Search, in CVPR 2011."

