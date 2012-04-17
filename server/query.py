import scipy as sp
import operator
from pylab import *
from numpy import *
from PIL import Image
from time import clock

from metadata import *
from pfutils import *

def getMatch(pb):
	debug('calculating hit map')
	pb = im2bw(pb).astype(int8)
	hm, unused = hitMap(pb)

	debug('searching')
	match = {}
	for theta in range(1, 7):
		for x, y, d in hm[theta]:
			if (x, y, theta) in mData.invIdx:
				for idx in mData.invIdx[(x, y, theta)]:
					if not idx in match:
						match[idx] = 1
					else:
						match[idx] += 1

	debug('matching')
	for idx in match:
		match[idx] = float(match[idx]) / mData.i2olen[idx]

	sorted_m = sorted(match.iteritems(), key = operator.itemgetter(1), reverse = True)

	return match, sorted_m

def debug_t(msg):
	debug('time used: %f' % (clock() - debug_t.tstamp))
	debug(msg)
	debug_t.tstamp = clock()
debug_t.tstamp = clock()

def test():
	debug('loading database')
	# mData = MetaData()
	# mData.load()

	debug_t('loading mat file')

	matname = '../data/teapot/22.mat'
	data = sp.io.loadmat(matname)
	pb = data['pb']

	debug_t('one side match')

	match, sorted_m = getMatch(pb)

	debug_t('finish one side match')

	if True:
		name = matname[:-3] + 'jpg'
		debug('origin: image %s score: %f' % (name, match[mData.name2i[name]]))
		figure()
		imshow(array(Image.open(name)))
		axis('off')

	debug_t('two side match')

	pb = im2bw(pb).astype(int8)
	qocm = extractOCM(pb)
	for ind, score1 in sorted_m[:min(len(sorted_m), 2000)]:
		hmap = mData.i2hmap[ind]
		score2 = 0
		for x, y, theta in qocm:
			if x < hmap[theta].shape[0] and y < hmap[theta].shape[1] and hmap[theta][x][y]:
				score2 += 1
		score2 = float(score2) / len(qocm)
		match[ind] = sqrt(score1 * score2)

	sorted_m = sorted(match.iteritems(), key = operator.itemgetter(1), reverse = True)

	debug_t('finish two side match')

	if True:
		figure()
		lenRes = 30
		for i in range(lenRes):
			imname = mData.i2name[sorted_m[i][0]]
			debug('name: %s score: %f' % (imname, sorted_m[i][1]))
			subplot(5, 6, i + 1)
			imshow(array(Image.open(imname)))
			axis('off')
		show()

if __name__ == '__main__':
	test()
