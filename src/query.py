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

	matname = '../data/gun/1.mat'
	# matname = 'butterfly.mat'
	data = sp.io.loadmat(matname)
	pb = data['pb']

	query(mData, pb)

def query(mData, pb):
	debug_t('one side match')

	pb = im2bw(pb).astype(uint8)
	qocm = extractOCM(pb)
	match, sorted_m = getMatch(mData, pb, qocm)

	debug_t('two side match')

	sorted_m = getMatch2(mData, qocm, sorted_m, match, 200)

	debug_t('finish two side match')

	lenRes = 30
	imnames = []
	for i in range(lenRes):
		imnames.append(mData.i2name[sorted_m[i][0]])

	if False:
		figure()
		gray()
		imshow(pb)
		axis('off')

		figure()
		for i in range(lenRes):
			imname = mData.i2name[sorted_m[i][0]]
			debug('name: %s score: %f' % (imname, sorted_m[i][1]))
			subplot(5, 6, i + 1)
			imshow(array(Image.open(imname)))
			axis('off')
		show()

	return imnames

if __name__ == '__main__':
	test()
	# profile.run('test()')
