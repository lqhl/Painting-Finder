import scipy as sp
import operator
from pylab import *
from numpy import *
from PIL import Image
from time import clock
import cProfile as profile

from metadata import *
try:
	from cpfutils import *
except:
	from pfutils import *

def debug_t(msg):
	debug('time used: %f' % (clock() - debug_t.tstamp))
	debug(msg)
	debug_t.tstamp = clock()
debug_t.tstamp = clock()

def test():
	debug('loading database')
	mData = MetaData()
	mData.load()

	debug_t('loading mat file')

	# matname = '../data/gun/1.mat'
	# data = sp.io.loadmat(matname)
	# pb = data['pb']

	pb = (255 - array(Image.open('test.jpg'))) / 255.0

	imnames = query(mData, pb)

	if True:
		figure()
		subplot(5, 6, 1)
		gray()
		imshow(pb)
		axis('off')

		# figure()
		for i, imname in enumerate(imnames[:29]):
			subplot(5, 6, i + 2)
			imshow(array(Image.open(imname)))
			axis('off')
		show()


def query(mData, pb):
	debug_t('one side match')

	pb = im2bw(pb).astype(uint8)
	qocm = extractOCM(pb)
	match, sorted_m = getMatch(mData, pb, qocm)

	debug_t('two side match')

	sorted_m = getMatch2(mData, qocm, sorted_m, match, 500)

	debug_t('finish two side match')

	lenRes = 30
	imnames = []
	for i in range(min(lenRes, len(sorted_m))):
		imname = mData.i2name[sorted_m[i][0]]
		imnames.append(imname)
		debug('name: %s, score: %f' % (imname, sorted_m[i][1]))

	return imnames

if __name__ == '__main__':
	test()
	# profile.run('test()')
