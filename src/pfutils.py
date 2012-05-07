from numpy import *
import operator

def debug(msg):
	print 'debug_pf: ', msg

edge_threshold = 0.1

def pyim2bw(x):
	if x >= edge_threshold:
		return 1
	else:
		return 0

im2bw = frompyfunc(pyim2bw, 1, 1)

def pyangle2c(x):
	if x < 0:
		x += pi

	if pi / 12 <= x < pi / 4:
		x = 1
	elif pi / 4 <= x < 5 * pi / 12:
		x = 2
	elif 5 * pi / 12 <= x < 7 * pi / 12:
		x = 3
	elif 7 * pi / 12 <= x < 3 * pi / 4:
		x = 4
	elif 3 * pi / 4 <= x < 11 * pi / 12:
		x = 5
	elif x < pi / 12 or x >= 11 * pi / 12:
		x = 6

	return x

angle2c = frompyfunc(pyangle2c, 1, 1)

def extractOCM(pb):
	px, py = gradient(pb)
	pa = arctan2(py, px)
	pa = angle2c(pa)
	ocm = []
	for i in range(pb.shape[0]):
		for j in range(pb.shape[1]):
			if pb[i][j] == 1:
				ocm.append((i, j, pa[i][j]))
	return ocm

# using the same radius (8) in CAO Yang's master thesis
radius = 8

__dx = [ 1,-1, 0, 0]
__dy = [ 0, 0, 1,-1]

def hitMap(pb, ocm):
	q = {}

	hmap = {}
	for theta in range(1, 7):
		b = zeros(pb.shape, dtype = int8)
		q[theta] = []

		for x, y, t in ocm:
			if t == theta:
				q[theta].append((x, y, 0))
				b[x, y] = 1

		i = 0
		while i < len(q[theta]):
			tx, ty, td = q[theta][i]
			if td < radius:
				for k in range(4):
					x = tx + __dx[k]
					y = ty + __dy[k]
					if 0 <= x < pb.shape[0] and 0 <= y < pb.shape[1] and not b[x][y]:
						b[x][y] = 1
						q[theta].append((x, y, td + 1))
			i += 1

		hmap[theta] = b

	return q, hmap

def getMatch(mData, pb, ocm):
	hm, unused = hitMap(pb, ocm)

	match = {}
	for theta in range(1, 7):
		for x, y, d in hm[theta]:
			if (x, y, theta) in mData.invIdx:
				for idx in mData.invIdx[(x, y, theta)]:
					if not idx in match:
						match[idx] = 1
					else:
						match[idx] += 1

	for idx in match:
		match[idx] = float(match[idx]) / mData.i2olen[idx]

	sorted_m = sorted(match.iteritems(), key = operator.itemgetter(1), reverse = True)

	return match, sorted_m

def getMatch2(mData, qocm, sorted_m, match, topN):
	qocm_len = len(qocm)
	for ind, score1 in sorted_m[:min(len(sorted_m), topN)]:
		hmap = mData.i2hmap[ind]
		score2 = 0
		for x, y, theta in qocm:
			if x < hmap[theta].shape[0] and y < hmap[theta].shape[1] and hmap[theta][x][y]:
				score2 += 1
		score2 = float(score2) / qocm_len
		match[ind] = math.sqrt(score1 * score2)

	sorted_m = sorted(match.iteritems(), key = operator.itemgetter(1), reverse = True)

	return sorted_m

