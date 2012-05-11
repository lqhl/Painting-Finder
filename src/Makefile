all: cpfutils.so

cpfutils.c: cpfutils.pyx
	cython cpfutils.pyx
cpfutils.so: cpfutils.c
	#gcc -shared -pthread -fPIC -fwrapv -O2 -Wall -fno-strict-aliasing -I/usr/include/python2.7 -o cpfutils.so cpfutils.c
	gcc -shared -pthread -fPIC -fwrapv -O2 -Wall -fno-strict-aliasing -I/usr/include/python2.7 -I/usr/local/lib/python2.7/dist-packages/numpy/core/include -o cpfutils.so cpfutils.c
