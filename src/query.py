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

	fnames = ['test%d.jpg' % i for i in range(1, 7)]
	figure(figsize = (30, 18))
	for i, fname in enumerate(fnames):
		pb = (255 - array(Image.open(fname))) / 255.0

		imnames = query(mData, pb)

		subplot(6, 10, i * 10 + 1)
		gray()
		imshow(pb)
		axis('off')

		# figure()
		for j, imname in enumerate(imnames[:9]):
			subplot(6, 10, i * 10 + 2 + j)
			imshow(array(Image.open(imname)))
			axis('off')
	savefig('6-result.eps')

def test2():
	debug('loading database')
	mData = MetaData()
	mData.load()

	debug_t('loading mat file')


	fnames = ['apple', 'pisa tower', 'eiffel tower', 'golden gate', 'butterfly', 'teapot']
	figure(figsize = (30, 18))
	for i, fname in enumerate(fnames):
		matname = '../data/%s/3.mat' % fname
		data = sp.io.loadmat(matname)
		pb = data['pb']
		pb = normalize(pb)

		imnames = query(mData, pb)

		subplot(6, 10, i * 10 + 1)
		gray()
		imshow(pb)
		axis('off')

		# figure()
		for j, imname in enumerate(imnames[:9]):
			subplot(6, 10, i * 10 + 2 + j)
			imshow(array(Image.open(imname)))
			axis('off')
	savefig('6-result.eps')

def query(mData, pb):
	debug_t('one side match')

	pb = im2bw(pb).astype(uint8)
	qocm = extractOCM(pb)
	match, sorted_m = getMatch(mData, pb, qocm)

	debug_t('two side match')

	#sorted_m = getMatch2(mData, qocm, sorted_m, match, 200)

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
