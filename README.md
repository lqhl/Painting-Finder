PaintingFinder
==============

The PaintingFinder is my final year project at Shanghai Jiao Tong University. It can search similar pictures of a sketch in database. You can considered it as an implementation of [MindFinder: Finding Images by Sketching](http://research.microsoft.com/en-us/projects/mindfinder/). You may refer to [Cao's paper][1] for implementation details.

Prerequisites
-------------

This project is developed with Python 2.7 under Ubuntu 12.04, and I have tested on Windows 7 too. The following libraries are required: PyGame, NumPy, SciPy, matplotlib, Python Image Library, Cython (optional). For Windows, I suggest you to install [pythonxy](http://code.google.com/p/pythonxy/) and PyGame.

Dataset
-------

The dataset is collected by [Rong Zhou](http://bcmi.sjtu.edu.cn/~zhourong/). I use Benchmark and Boundary Detection Code on [The Berkeley Segmentation Dataset and Benchmark](http://www.eecs.berkeley.edu/Research/Projects/CS/vision/grouping/segbench/) to get the sketch of each picture in the dataset.

Building Index
--------------

To build binary file (optional if you don't have Cython):

    cd src
    make

To build the index of dataset in folder `/data`:

    python build_index.py

It may takes several minutes.

Usage
-----

To draw a sketch and find similar pictures:

    python painter.py

You can clean the board by pressing `c`, and quit by pressing `q`.

Contact
-------

Author: Qin Liu  
Email: lqgy2001@gmail.com  
Url: http://www.cse.cuhk.edu.hk/~qliu

[1]: http://research.microsoft.com/apps/pubs/?id=149199 "Yang Cao, Changhu Wang, Liqing Zhang, and Lei Zhang, Edgel Inverted Index for Large-Scale Sketch-based Image Search, in CVPR 2011."

