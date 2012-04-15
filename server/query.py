import pickle
import scipy as sp
import operator
from pylab import *
from numpy import *
from PIL import Image

from metadata import *
from pfutils import *

debugging = False

# using the same radius in CAO Yang's master thesis
radius = 3

__dx = [ 1,-1, 0, 0]
__dy = [ 0, 0, 1,-1]

def hitMap(pb):
	q = {}
	ocm = extractOCM(pb)
	row = range(pb.shape[0])
	col = range(pb.shape[1])
	debug(str(pb.shape[0] * pb.shape[1]))

	for theta in range(1, 7):
		b = zeros(pb.shape)
		q[theta] = []

		for x, y, t in ocm:
			if t == theta:
				q[theta].append((x, y, 0))
				b[x, y] = 1

		debug('init length: %d' % len(q[theta]))
		i = 0
		while i < len(q[theta]):
			tx, ty, td = q[theta][i]
			if td < radius:
				for k in range(4):
					x = tx + __dx[k]
					y = ty + __dy[k]
					if x in row and y in col and not b[x][y]:
						b[x][y] = 1
						q[theta].append((x, y, td + 1))
			i += 1
		debug('length: %d' % i)
	if debugging:
		figure()
		gray()
		imshow(b)
		figure()
		gray()
		imshow(pb)
		show()
	return q

def getMatch(pb):
	debug('calculating hit map')
	hm = hitMap(pb)

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

def test():
	debug('loading database')
	#with open('db.pkl', 'rb') as f:
	#	mData = pickle.load(f)

	debug('loading mat file')
	matname = '../data/swan/5.mat'
	data = sp.io.loadmat(matname)
	pb = data['pb']

	match, sorted_m = getMatch(pb)
	debug('length of sorted_m: %d' % len(sorted_m))
	for each in sorted_m(:max(len, 1000)):
		pass

	if debugging:
		name = matname[:-3] + 'jpg'
		debug(str(sorted_m[:10]))
		debug('origin: image %s score: %f' % (name, match[mData.name2i[name]]))
		figure()
		imshow(array(Image.open(name)))
		for i in range(10):
			name = mData.i2name[sorted_m[i][0]]
			debug('name: %s score: %f' % (name, sorted_m[i][1]))
			#figure()
			#imshow(array(Image.open(name)))
		show()

	return

if __name__ == '__main__':
	test()
